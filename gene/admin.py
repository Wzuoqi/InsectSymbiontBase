from django.contrib import admin
from .models import Gene

@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ('gene_id', 'source_id', 'nr_annotation', 'nr_species', 'cog_category')
    list_filter = ('source_id', 'nr_species', 'cog_category')
    search_fields = ('gene_id', 'nr_annotation', 'nr_species', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('source_id', 'gene_id', 'sequence', 'gene_length')
        }),
        ('DIAMOND Results', {
            'fields': (
                'nr_id', 'identity', 'alignment_length', 'mismatches', 'gap_openings',
                'query_start', 'query_end', 'subject_start', 'subject_end',
                'evalue', 'bit_score', 'nr_annotation', 'nr_species'
            )
        }),
        ('eggNOG Annotation', {
            'fields': (
                'seed_ortholog', 'eggnog_evalue', 'eggnog_score', 'eggnog_ogs',
                'max_annot_lvl', 'cog_category', 'description', 'preferred_name',
                'go_terms', 'ec_number', 'kegg_ko', 'kegg_pathway', 'kegg_module',
                'kegg_reaction', 'kegg_rclass', 'brite', 'kegg_tc', 'cazy',
                'bigg_reaction', 'pfams'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        })
    )
