from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Gene
import logging

logger = logging.getLogger(__name__)

@registry.register_document
class GeneDocument(Document):
    """
    Gene Elasticsearch Document

    这个文档类将 Gene 模型映射到 Elasticsearch 索引
    """
    # 修改字段类型，使其支持部分匹配
    host = fields.TextField(
        fields={'keyword': fields.KeywordField()}  # 保留keyword子字段用于精确匹配
    )
    source_id = fields.TextField(
        fields={'keyword': fields.KeywordField()}
    )
    gene_id = fields.TextField(
        fields={'keyword': fields.KeywordField()}
    )
    nr_id = fields.TextField(
        null=True,
        fields={'keyword': fields.KeywordField()}
    )

    # 文本字段 - 用于全文搜索
    nr_annotation = fields.TextField(null=True)
    nr_species = fields.TextField(null=True)
    description = fields.TextField(null=True)
    preferred_name = fields.TextField(null=True)

    # 功能注释字段
    seed_ortholog = fields.TextField(null=True)
    go_terms = fields.TextField(null=True)
    ec_number = fields.TextField(null=True)
    kegg_ko = fields.TextField(null=True)
    kegg_pathway = fields.TextField(null=True)
    pfams = fields.TextField(null=True)
    cog_category = fields.TextField(null=True)

    # 数值字段
    identity = fields.FloatField(null=True)
    bit_score = fields.FloatField(null=True)
    evalue = fields.FloatField(null=True)
    gene_length = fields.IntegerField(null=True)

    class Index:
        # 使用现有的索引名称
        name = 'genes'
        # 索引设置
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Gene  # 关联的 Django 模型
        # 不需要在这里指定字段，因为我们已经手动映射了所有需要的字段

        # 由于我们使用的是现有索引，不需要自动同步
        # 如果需要重建索引，可以设置为 True
        ignore_signals = True
        auto_refresh = False

    def prepare(self, instance):
        try:
            data = super().prepare(instance)
            return data
        except Exception as e:
            logger.error(f"Error preparing document for instance {instance.id}: {str(e)}")
            raise