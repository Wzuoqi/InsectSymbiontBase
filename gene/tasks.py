from celery import shared_task
import csv
import os
from django.conf import settings
from django.core.mail import send_mail
import datetime

@shared_task
def index_gene_chunk(start, end):
    docs = []
    genes = Gene.objects.all()[start:end]
    for gene in genes:
        try:
            doc = {
                '_index': 'genes',
                '_id': gene.id,
                '_source': GeneDocument.prepare(GeneDocument(), gene)
            }
            docs.append(doc)
        except Exception as e:
            logger.error(f"Error processing gene {gene.id}: {str(e)}")

    if docs:
        bulk(connections.get_connection(), docs)
    return len(docs)

@shared_task
def generate_large_gene_download(search_params, user_email):
    """
    异步生成大型基因搜索结果文件
    """
    # 构建与下载视图相同的查询
    # ...

    # 创建临时文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"gene_search_results_{timestamp}.tsv"
    filepath = os.path.join(settings.MEDIA_ROOT, 'downloads', filename)

    # 确保目录存在
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 使用 scroll API 处理大量结果
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')

        # 写入表头
        # ...

        # 使用 scroll API 批量获取结果
        # ...

    # 生成下载链接
    download_url = f"{settings.SITE_URL}/media/downloads/{filename}"

    # 发送电子邮件
    send_mail(
        'Your Gene Search Results are Ready',
        f'Your gene search results are ready for download: {download_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    return filepath