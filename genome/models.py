from django.db import models

class Genome(models.Model):
    id = models.AutoField(primary_key=True)
    genome_id = models.CharField(max_length=100, unique=True, db_index=True)
    metagenome_id = models.CharField(max_length=100, blank=True, null=True)

    host = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    function = models.TextField(blank=True, null=True)
    literature_name = models.CharField(max_length=200, blank=True, null=True)
    reference = models.CharField(max_length=200, blank=True, null=True)

    checkm_marker_lineage = models.CharField(max_length=200, blank=True, null=True)
    checkm_genomes = models.IntegerField(blank=True, null=True)
    checkm_markers = models.IntegerField(blank=True, null=True)
    completeness = models.FloatField(blank=True, null=True)
    contamination = models.FloatField(blank=True, null=True)
    strain_heterogeneity = models.FloatField(blank=True, null=True)
    quality_score = models.FloatField(blank=True, null=True)

    gtdb_classification = models.TextField(blank=True, null=True)
    gtdb_phylum = models.CharField(max_length=100, blank=True, null=True)

    closest_genome_reference = models.CharField(max_length=100, blank=True, null=True)
    closest_genome_reference_radius = models.FloatField(blank=True, null=True)
    closest_genome_ani = models.FloatField(blank=True, null=True)
    closest_placement_reference = models.CharField(max_length=100, blank=True, null=True)

    classification_method = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.genome_id} - {self.host}"

    class Meta:
        ordering = ['host', 'genome_id']
        indexes = [
            models.Index(fields=['host', 'genome_id']),
        ]