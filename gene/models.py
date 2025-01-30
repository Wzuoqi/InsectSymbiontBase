from django.db import models

class Gene(models.Model):
    source_id = models.CharField(max_length=200, db_index=True)  # Source ID
    gene_id = models.CharField(max_length=200, db_index=True)  # Gene ID
    nr_id = models.CharField(max_length=200, null=True, blank=True)  # NR ID

    identity = models.FloatField(null=True, blank=True, default=0.0)  # Identity
    alignment_length = models.IntegerField(null=True, blank=True, default=0)  # Alignment Length
    mismatches = models.IntegerField(null=True, blank=True, default=0)  # mismatches
    gap_openings = models.IntegerField(null=True, blank=True, default=0)  # gap openings
    query_start = models.IntegerField(null=True, blank=True, default=0)  # q.start
    query_end = models.IntegerField(null=True, blank=True, default=0)  # q.end
    subject_start = models.IntegerField(null=True, blank=True, default=0)  # s.start
    subject_end = models.IntegerField(null=True, blank=True, default=0)  # s.end
    evalue = models.FloatField(null=True, blank=True, default=0.0)  # E-value
    bit_score = models.FloatField(null=True, blank=True, default=0.0)  # bit score
    sequence = models.TextField(default='')  # sequence
    gene_length = models.IntegerField(default=0)  # gene length

    nr_annotation = models.TextField(null=True, blank=True, default='')  # NR annotation
    nr_species = models.TextField(null=True, blank=True, default='')  # NR species

    seed_ortholog = models.TextField(null=True, blank=True, default='')  # seed_ortholog
    eggnog_evalue = models.FloatField(null=True, blank=True, default=0.0)  # evalue
    eggnog_score = models.FloatField(null=True, blank=True, default=0.0)  # score
    eggnog_ogs = models.TextField(null=True, blank=True, default='')  # eggNOG_OGs
    max_annot_lvl = models.TextField(null=True, blank=True, default='')  # max_annot_lvl
    cog_category = models.TextField(null=True, blank=True, default='')  # COG_category
    description = models.TextField(null=True, blank=True, default='')  # Description
    preferred_name = models.TextField(null=True, blank=True, default='')  # Preferred_name
    go_terms = models.TextField(null=True, blank=True, default='')  # GOs
    ec_number = models.TextField(null=True, blank=True, default='')  # EC
    kegg_ko = models.TextField(null=True, blank=True, default='')  # KEGG_ko
    kegg_pathway = models.TextField(null=True, blank=True, default='')  # KEGG_Pathway
    kegg_module = models.TextField(null=True, blank=True, default='')  # KEGG_Module
    kegg_reaction = models.TextField(null=True, blank=True, default='')  # KEGG_Reaction
    kegg_rclass = models.TextField(null=True, blank=True, default='')  # KEGG_rclass
    brite = models.TextField(null=True, blank=True, default='')  # BRITE
    kegg_tc = models.TextField(null=True, blank=True, default='')  # KEGG_TC
    cazy = models.TextField(null=True, blank=True, default='')  # CAZy
    bigg_reaction = models.TextField(null=True, blank=True, default='')  # BiGG_Reaction
    pfams = models.TextField(null=True, blank=True, default='')  # PFAMs

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gene_id} - {self.nr_annotation or 'Unknown'}"

    class Meta:
        indexes = [
            models.Index(fields=['source_id']),
            models.Index(fields=['nr_id'], name='custom_nr_id_idx'),
            models.Index(fields=['nr_species']),
            models.Index(fields=['cog_category']),
        ]
        unique_together = [('source_id', 'gene_id')]