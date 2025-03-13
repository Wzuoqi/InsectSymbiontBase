from django.core.management.base import BaseCommand
from elasticsearch_dsl import connections
from django_elasticsearch_dsl.registries import registry

class Command(BaseCommand):
    help = 'Rebuild the Elasticsearch index for Gene model'

    def handle(self, *args, **options):
        self.stdout.write('Rebuilding Gene index...')

        # 获取 Gene 文档
        gene_doc = registry.get_documents()[0]

        # 创建索引
        gene_doc._index.create()

        # 填充索引
        qs = gene_doc.get_queryset()
        self.stdout.write(f'Indexing {qs.count()} genes...')

        # 批量索引
        gene_doc.update(qs)

        self.stdout.write(self.style.SUCCESS('Successfully rebuilt Gene index'))