from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Gene
import logging

logger = logging.getLogger(__name__)

@registry.register_document
class GeneDocument(Document):
    # 只定义需要raw keyword字段的特殊字段
    host = fields.TextField(
        fields={'raw': fields.KeywordField()}
    )
    source_id = fields.TextField(
        fields={'raw': fields.KeywordField()}
    )
    gene_id = fields.TextField(
        fields={'raw': fields.KeywordField()}
    )
    nr_id = fields.TextField(
        fields={'raw': fields.KeywordField()}
    )

    # 这些字段需要全文搜索
    nr_annotation = fields.TextField(analyzer='ngram_analyzer')
    nr_species = fields.TextField(analyzer='ngram_analyzer')
    description = fields.TextField(analyzer='ngram_analyzer')
    preferred_name = fields.TextField(analyzer='ngram_analyzer')
    go_terms = fields.TextField(analyzer='ngram_analyzer')
    ec_number = fields.TextField(analyzer='ngram_analyzer')
    kegg_ko = fields.TextField(analyzer='ngram_analyzer')
    kegg_pathway = fields.TextField(analyzer='ngram_analyzer')
    pfams = fields.TextField(analyzer='ngram_analyzer')

    class Index:
        name = 'genes'
        settings = {
            'number_of_shards': 1,  # 改为单分片
            'number_of_replicas': 0,
            'refresh_interval': '30s',
            'index.max_ngram_diff': 7,
            'index.routing.allocation.total_shards_per_node': 3,
            'index.write.wait_for_active_shards': 1,
            'index.mapping.total_fields.limit': 2000,
            'index.translog.durability': 'async',
            'index.translog.sync_interval': '30s',
            'index.translog.flush_threshold_size': '256mb',
            'analysis': {
                'analyzer': {
                    'ngram_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'ngram_tokenizer',
                        'filter': ['lowercase']
                    }
                },
                'tokenizer': {
                    'ngram_tokenizer': {
                        'type': 'ngram',
                        'min_gram': 3,
                        'max_gram': 4,  # 先用小一点的差值
                        'token_chars': ['letter', 'digit']
                    }
                }
            }
        }

    class Django:
        model = Gene

        # 自动映射其他字段
        fields = [
            # 基本信息字段
            'identity',
            'alignment_length',
            'mismatches',
            'gap_openings',
            'query_start',
            'query_end',
            'subject_start',
            'subject_end',
            'evalue',
            'bit_score',
            'sequence',
            'gene_length',

            # EggNOG相关字段
            'seed_ortholog',
            'eggnog_evalue',
            'eggnog_score',
            'eggnog_ogs',
            'max_annot_lvl',

            # 功能注释字段
            'cog_category',
            'kegg_module',
            'kegg_reaction',
            'kegg_rclass',
            'kegg_tc',

            # 其他注释字段
            'brite',
            'cazy',
            'bigg_reaction',
        ]

    def prepare(self, instance):
        try:
            data = super().prepare(instance)
            return data
        except Exception as e:
            logger.error(f"Error preparing document for instance {instance.id}: {str(e)}")
            raise