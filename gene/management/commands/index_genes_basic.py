from django.core.management.base import BaseCommand
from django.db import connection
from gene.models import Gene
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
import logging
import time
import sys

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Basic indexing command with minimal dependencies'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=100)
        parser.add_argument('--start-from', type=int, default=0)
        parser.add_argument('--max-docs', type=int, default=None)
        parser.add_argument('--sleep', type=float, default=0.5, help='Sleep time between batches in seconds')

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        start_from = options['start_from']
        max_docs = options['max_docs']
        sleep_time = options['sleep']

        # 获取总记录数
        total = Gene.objects.count()
        if max_docs:
            total = min(total, start_from + max_docs)

        self.stdout.write(f"Starting indexing from position {start_from} with batch size {batch_size}")
        self.stdout.write(f"Total records to process: {total - start_from}")

        # 获取 Elasticsearch 连接
        es = connections.get_connection()

        processed = 0
        successful = 0
        failed = 0
        start_time = time.time()
        last_report_time = start_time

        # 处理每个批次
        for start in range(start_from, total, batch_size):
            end = min(start + batch_size, total)

            # 每10秒输出一次进度
            current_time = time.time()
            if current_time - last_report_time >= 10:
                elapsed = current_time - start_time
                rate = processed / elapsed if elapsed > 0 else 0
                eta_seconds = (total - start_from - processed) / rate if rate > 0 else 0
                eta_hours = eta_seconds / 3600

                self.stdout.write(
                    f"Progress: {processed:,}/{total-start_from:,} "
                    f"({processed/(total-start_from)*100:.1f}%) | "
                    f"Position: {start:,} | "
                    f"Rate: {rate:.1f} docs/sec | "
                    f"ETA: {eta_hours:.1f} hours | "
                    f"Success: {successful:,} | "
                    f"Failed: {failed:,}"
                )
                last_report_time = current_time

                # 强制刷新输出
                sys.stdout.flush()

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
                        self.stderr.write(f"Error processing gene {gene.get('id')}: {str(e)}")
                        failed += 1

                # 批量索引
                success = False
                for retry in range(3):  # 最多重试3次
                    try:
                        success_count, errors = bulk(
                            es,
                            docs,
                            chunk_size=min(batch_size, 100),  # 使用更小的块大小
                            raise_on_error=False,
                            request_timeout=60
                        )
                        successful += success_count
                        if errors:
                            failed += len(errors)
                            self.stderr.write(f"Errors in bulk operation: {len(errors)}")
                        success = True
                        break
                    except Exception as e:
                        self.stderr.write(f"Bulk operation failed (attempt {retry+1}/3): {str(e)}")
                        if retry < 2:  # 如果不是最后一次尝试
                            time.sleep(5)  # 固定等待5秒

                # 更新处理计数
                batch_size_actual = len(genes)
                processed += batch_size_actual

                # 清理连接
                connection.close()

                # 在批次之间休眠一小段时间，减轻服务器负担
                if sleep_time > 0:
                    time.sleep(sleep_time)

            except Exception as e:
                self.stderr.write(f"Error processing batch {start}-{end}: {str(e)}")
                failed += batch_size

                # 尝试清理连接
                try:
                    connection.close()
                except:
                    pass

                # 出错后等待更长时间
                time.sleep(10)

        # 计算总时间
        total_time = time.time() - start_time
        hours = total_time / 3600

        # 输出最终统计信息
        self.stdout.write(
            f"\nIndexing completed in {hours:.2f} hours!\n"
            f"Total processed: {processed:,}\n"
            f"Successfully indexed: {successful:,}\n"
            f"Failed: {failed:,}\n"
            f"Average rate: {processed/total_time:.1f} docs/sec"
        )