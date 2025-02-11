from django.db import models

class Symbiont(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    record_type = models.CharField(max_length=100, null=True, blank=True)

    # host
    host_order = models.CharField(max_length=100, null=True, blank=True)
    host_family = models.CharField(max_length=100, db_index=True, default="NA")
    host_subfamily = models.CharField(max_length=100, blank=True, null=True, db_index=True, default="NA")
    host_species = models.CharField(max_length=100, blank=True, null=True, db_index=True, default="NA")
    # symbiont
    symbiont_phylum = models.CharField(max_length=100, blank=True, null=True, default="NA")
    symbiont_order = models.CharField(max_length=100, blank=True, null=True, default="NA")
    symbiont_genus = models.CharField(max_length=100, blank=True, null=True, default="NA")
    symbiont_rank = models.CharField(max_length=100, blank=True, null=True, default="NA")
    symbiont_taxon = models.CharField(max_length=200, blank=True, null=True, default="NA")
    symbiont_name = models.CharField(max_length=200, blank=True, null=True, db_index=True, default="NA")
    classification = models.CharField(max_length=100, default="NA")
    # funcion
    localization = models.CharField(max_length=100, default="NA")
    transmission_mode = models.CharField(max_length=100, default="NA")
    function = models.TextField(blank=True, null=True, default="NA")
    function_tag = models.CharField(max_length=200, blank=True, null=True, default="NA")
    related_accession = models.CharField(max_length=2000, blank=True, null=True, default="NA")
    # literature
    reference = models.TextField(blank=True, null=True, default="NA")
    doi = models.CharField(max_length=200, blank=True, null=True, default="NA")
    journal = models.CharField(max_length=200, blank=True, null=True, default="NA")
    year = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True, default="NA")

    # 新增genome_id字段
    genome_id = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f"{self.symbiont_name} - {self.host_species} ({self.host_order})"

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['host_order', 'host_family', 'host_species']),
            models.Index(fields=['symbiont_name']),
            models.Index(fields=['year']),
        ]
