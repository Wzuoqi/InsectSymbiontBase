from django.core.management.base import BaseCommand
from django.db import connection
from gene.models import Gene
from gene.documents import GeneDocument
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from tqdm import tqdm
import logging
from concurrent.futures import ThreadPoolExecutor
import time
from elasticsearch import TransportError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Index genes in batches with progress bar'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=1000)
        parser.add_argument('--threads', type=int, default=4)
        parser.add_argument('--queue-size', type=int, default=8)
        parser.add_argument('--retry-count', type=int, default=3)

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        thread_count = options['threads']
        queue_size = options['queue_size']
        retry_count = options['retry_count']

        def bulk_with_retry(es, docs, max_retries=3):
            for attempt in range(max_retries):
                try:
                    return bulk(
                        es,
                        docs,
                        chunk_size=min(batch_size, 1000),
                        raise_on_error=False,
                        request_timeout=60,
                        timeout='60s'
                    )
                except TransportError as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Bulk operation failed (attempt {attempt+1}/{max_retries}): {str(e)}")
                    time.sleep(2 ** attempt)
                    continue

        def process_batch(genes):
            docs = []
            for gene in genes:
                try:
                    doc = {
                        '_index': 'genes',
                        '_id': gene['id'],
                        '_source': {
                            'host': gene['host'],
                            'source_id': gene['source_id'],
                            'gene_id': gene['gene_id'],
                            'nr_id': gene['nr_id'],
                            'nr_annotation': gene['nr_annotation'],
                            'description': gene['description'],
                            'identity': gene['identity'],
                            'alignment_length': gene['alignment_length'],
                            'mismatches': gene['mismatches'],
                            'gap_openings': gene['gap_openings'],
                            'query_start': gene['query_start'],
                            'query_end': gene['query_end'],
                            'subject_start': gene['subject_start'],
                            'subject_end': gene['subject_end'],
                            'evalue': gene['evalue'],
                            'bit_score': gene['bit_score'],
                            'sequence': gene['sequence'],
                            'gene_length': gene['gene_length'],
                            'seed_ortholog': gene['seed_ortholog'],
                            'eggnog_evalue': gene['eggnog_evalue'],
                            'eggnog_score': gene['eggnog_score'],
                            'eggnog_ogs': gene['eggnog_ogs'],
                            'max_annot_lvl': gene['max_annot_lvl'],
                            'cog_category': gene['cog_category'],
                            'kegg_module': gene['kegg_module'],
                            'kegg_reaction': gene['kegg_reaction'],
                            'kegg_rclass': gene['kegg_rclass'],
                            'kegg_tc': gene['kegg_tc'],
                            'brite': gene['brite'],
                            'cazy': gene['cazy'],
                            'bigg_reaction': gene['bigg_reaction'],
                            'go_terms': gene['go_terms'],
                            'ec_number': gene['ec_number'],
                            'kegg_ko': gene['kegg_ko'],
                            'kegg_pathway': gene['kegg_pathway'],
                            'pfams': gene['pfams'],
                            'nr_species': gene['nr_species'],
                            'preferred_name': gene['preferred_name']
                        }
                    }
                    docs.append(doc)
                except Exception as e:
                    logger.error(f"Error processing gene {gene.get('id')}: {str(e)}")
            return docs

        def get_batches():
            total = Gene.objects.count()
            with tqdm(total=total, desc="Indexing") as pbar:
                for start in range(0, total, batch_size):
                    try:
                        genes = list(Gene.objects.all().values(
                            'id', 'host', 'source_id', 'gene_id', 'nr_id',
                            'nr_annotation', 'description', 'identity',
                            'alignment_length', 'mismatches', 'gap_openings',
                            'query_start', 'query_end', 'subject_start',
                            'subject_end', 'evalue', 'bit_score', 'sequence',
                            'gene_length', 'seed_ortholog', 'eggnog_evalue',
                            'eggnog_score', 'eggnog_ogs', 'max_annot_lvl',
                            'cog_category', 'kegg_module', 'kegg_reaction',
                            'kegg_rclass', 'kegg_tc', 'brite', 'cazy',
                            'bigg_reaction', 'go_terms', 'ec_number',
                            'kegg_ko', 'kegg_pathway', 'pfams', 'nr_species',
                            'preferred_name'
                        )[start:start + batch_size])
                        yield genes
                        pbar.update(len(genes))
                    except Exception as e:
                        logger.error(f"Error fetching batch starting at {start}: {str(e)}")
                        continue

        try:
            es = connections.get_connection()

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = []
                for genes_batch in get_batches():
                    while len(futures) >= queue_size:
                        done_futures = [f for f in futures if f.done()]
                        for completed in done_futures:
                            try:
                                docs = completed.result()
                                if docs:
                                    bulk_with_retry(es, docs, retry_count)
                            except Exception as e:
                                logger.error(f"Error in bulk operation: {str(e)}")
                            futures.remove(completed)
                        if len(futures) >= queue_size:
                            time.sleep(0.1)

                    future = executor.submit(process_batch, genes_batch)
                    futures.append(future)

                for future in futures:
                    try:
                        docs = future.result()
                        if docs:
                            bulk_with_retry(es, docs, retry_count)
                    except Exception as e:
                        logger.error(f"Error in final bulk operation: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

        finally:
            connection.close()

        # 输出内存使用统计
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        self.stdout.write(
            f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB"
        )