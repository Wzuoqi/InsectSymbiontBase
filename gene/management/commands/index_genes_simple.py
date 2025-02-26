from django.core.management.base import BaseCommand
from django.db import connection
from gene.models import Gene
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from tqdm import tqdm
import logging
import time
import psutil
from elasticsearch import TransportError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Index genes in batches with simple approach'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=500)
        parser.add_argument('--start-from', type=int, default=0, help='Start indexing from this position')
        parser.add_argument('--max-docs', type=int, default=None, help='Maximum number of documents to index')

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        start_from = options['start_from']
        max_docs = options['max_docs']

        # 获取总记录数
        total = Gene.objects.count()
        if max_docs:
            total = min(total, start_from + max_docs)

        self.stdout.write(f"Starting indexing from position {start_from} with batch size {batch_size}")
        self.stdout.write(f"Total records to process: {total - start_from}")

        # 获取 Elasticsearch 连接
        es = connections.get_connection()

        # 初始化进度条
        with tqdm(total=total - start_from, desc="Indexing") as pbar:
            processed = 0
            successful = 0
            failed = 0

            # 处理每个批次
            for start in range(start_from, total, batch_size):
                end = min(start + batch_size, total)

                # 记录批次开始时间
                batch_start_time = time.time()

                try:
                    # 获取当前批次的数据
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
                    )[start:end])

                    # 准备文档
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
                            failed += 1

                    # 批量索引
                    success = False
                    for retry in range(5):  # 最多重试5次
                        try:
                            success_count, errors = bulk(
                                es,
                                docs,
                                chunk_size=min(batch_size, 500),
                                raise_on_error=False,
                                request_timeout=120,  # 增加超时时间
                                timeout='120s'
                            )
                            successful += success_count
                            failed += len(errors) if errors else 0
                            success = True
                            break
                        except TransportError as e:
                            logger.warning(f"Bulk operation failed (attempt {retry+1}/5): {str(e)}")
                            if retry < 4:  # 如果不是最后一次尝试
                                wait_time = 2 ** retry
                                logger.info(f"Waiting {wait_time} seconds before retry...")
                                time.sleep(wait_time)
                            else:
                                logger.error(f"Failed to index batch after 5 attempts: {str(e)}")
                                failed += len(docs)

                    # 如果所有重试都失败
                    if not success:
                        logger.error(f"Failed to index batch {start}-{end} after all retries")

                    # 更新进度条
                    batch_size_actual = len(genes)
                    processed += batch_size_actual
                    pbar.update(batch_size_actual)

                    # 计算批次处理时间和速率
                    batch_time = time.time() - batch_start_time
                    rate = batch_size_actual / batch_time if batch_time > 0 else 0

                    # 每10个批次输出一次统计信息
                    if (start - start_from) % (batch_size * 10) == 0:
                        # 获取内存使用情况
                        process = psutil.Process()
                        memory_info = process.memory_info()
                        memory_mb = memory_info.rss / 1024 / 1024

                        self.stdout.write(
                            f"Position: {start:,}/{total:,} "
                            f"({start/total*100:.1f}%) | "
                            f"Rate: {rate:.1f} docs/sec | "
                            f"Success: {successful:,} | "
                            f"Failed: {failed:,} | "
                            f"Memory: {memory_mb:.1f} MB"
                        )

                    # 清理连接
                    connection.close()

                except Exception as e:
                    logger.error(f"Error processing batch {start}-{end}: {str(e)}")
                    failed += batch_size
                    pbar.update(batch_size)  # 即使失败也更新进度条

                    # 尝试清理连接
                    try:
                        connection.close()
                    except:
                        pass

        # 输出最终统计信息
        self.stdout.write(self.style.SUCCESS(
            f"\nIndexing completed!\n"
            f"Total processed: {processed:,}\n"
            f"Successfully indexed: {successful:,}\n"
            f"Failed: {failed:,}"
        ))