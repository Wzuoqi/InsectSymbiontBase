from django.core.management.base import BaseCommand
from django.db import connection
from gene.models import Gene
from elasticsearch.helpers import bulk, streaming_bulk
from elasticsearch_dsl.connections import connections
import logging
import time
import sys
from elasticsearch import TransportError, ConnectionTimeout

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Optimized indexing command for large datasets'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=200)
        parser.add_argument('--start-from', type=int, default=0)
        parser.add_argument('--max-docs', type=int, default=None)
        parser.add_argument('--chunk-size', type=int, default=50)
        parser.add_argument('--timeout', type=int, default=120)

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        start_from = options['start_from']
        max_docs = options['max_docs']
        chunk_size = options['chunk_size']
        timeout = options['timeout']

        # 获取总记录数
        total = Gene.objects.count()
        if max_docs:
            total = min(total, start_from + max_docs)

        self.stdout.write(f"Starting indexing from position {start_from} with batch size {batch_size}")
        self.stdout.write(f"Total records to process: {total - start_from}")
        self.stdout.write(f"Using chunk size: {chunk_size}, timeout: {timeout}s")

        # 获取 Elasticsearch 连接
        es = connections.get_connection()

        # 检查 Elasticsearch 设置
        try:
            index_settings = es.indices.get_settings(index="genes")
            refresh_interval = index_settings.get("genes", {}).get("settings", {}).get("index", {}).get("refresh_interval", "1s")
            replicas = index_settings.get("genes", {}).get("settings", {}).get("index", {}).get("number_of_replicas", "1")

            self.stdout.write(f"Current index settings - refresh_interval: {refresh_interval}, replicas: {replicas}")

            # 如果需要，优化索引设置
            if refresh_interval != "30s" or replicas != "0":
                self.stdout.write("Optimizing index settings for bulk indexing...")
                es.indices.put_settings(
                    index="genes",
                    body={
                        "index": {
                            "refresh_interval": "30s",
                            "number_of_replicas": 0
                        }
                    }
                )
                self.stdout.write("Index settings updated.")
        except Exception as e:
            self.stderr.write(f"Warning: Could not check/update index settings: {str(e)}")

        processed = 0
        successful = 0
        failed = 0
        start_time = time.time()
        last_report_time = start_time

        # 使用生成器来准备文档
        def get_docs(start_pos, end_pos):
            try:
                genes = Gene.objects.all().values(
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
                )[start_pos:end_pos]

                for gene in genes:
                    try:
                        yield {
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
                    except Exception as e:
                        self.stderr.write(f"Error processing gene {gene.get('id')}: {str(e)}")
            finally:
                connection.close()

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
                sys.stdout.flush()

            # 使用 streaming_bulk 进行批量索引
            batch_success = 0
            batch_failed = 0

            try:
                # 使用 streaming_bulk 可以更好地控制每个文档的处理
                actions = get_docs(start, end)

                for ok, result in streaming_bulk(
                    es,
                    actions,
                    chunk_size=chunk_size,
                    request_timeout=timeout,
                    yield_ok=True,
                    raise_on_error=False,
                    max_retries=3
                ):
                    if ok:
                        batch_success += 1
                    else:
                        batch_failed += 1
                        error = result.get('index', {}).get('error', 'Unknown error')
                        self.stderr.write(f"Error indexing document: {error}")

                successful += batch_success
                failed += batch_failed
                processed += (batch_success + batch_failed)

            except ConnectionTimeout as e:
                self.stderr.write(f"Connection timeout at position {start}: {str(e)}")
                # 减小批量大小并重试
                retry_batch_size = batch_size // 2
                retry_chunk_size = chunk_size // 2

                if retry_batch_size > 0 and retry_chunk_size > 0:
                    self.stdout.write(f"Retrying with smaller batch size: {retry_batch_size}, chunk size: {retry_chunk_size}")

                    try:
                        # 重试这个批次，使用更小的批量大小
                        for sub_start in range(start, end, retry_batch_size):
                            sub_end = min(sub_start + retry_batch_size, end)

                            actions = get_docs(sub_start, sub_end)
                            sub_success = 0
                            sub_failed = 0

                            for ok, result in streaming_bulk(
                                es,
                                actions,
                                chunk_size=retry_chunk_size,
                                request_timeout=timeout * 2,  # 增加超时时间
                                yield_ok=True,
                                raise_on_error=False,
                                max_retries=5
                            ):
                                if ok:
                                    sub_success += 1
                                else:
                                    sub_failed += 1

                            successful += sub_success
                            failed += sub_failed
                            processed += (sub_success + sub_failed)

                            # 在子批次之间休眠
                            time.sleep(1)

                    except Exception as sub_e:
                        self.stderr.write(f"Error during retry at position {start}: {str(sub_e)}")
                        failed += (end - start) - (successful - batch_success)
                        processed += (end - start) - (processed - (batch_success + batch_failed))
                else:
                    # 如果批量大小已经很小，就跳过这个批次
                    self.stderr.write(f"Skipping batch at position {start}")
                    failed += (end - start)
                    processed += (end - start)

            except Exception as e:
                self.stderr.write(f"Error processing batch {start}-{end}: {str(e)}")
                failed += (end - start) - batch_success
                processed += (end - start) - (batch_success + batch_failed)

                # 出错后等待
                time.sleep(5)

        # 恢复索引设置
        try:
            self.stdout.write("Restoring index settings...")
            es.indices.put_settings(
                index="genes",
                body={
                    "index": {
                        "refresh_interval": "1s",
                        "number_of_replicas": 1
                    }
                }
            )
            self.stdout.write("Index settings restored.")
        except Exception as e:
            self.stderr.write(f"Warning: Could not restore index settings: {str(e)}")

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