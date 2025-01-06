from django.db import models

class Genome(models.Model):
    genome_id = models.CharField(max_length=100, primary_key=True)
    source_id = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    host = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    function = models.TextField(blank=True, null=True)

    reference_name = models.CharField(max_length=200, blank=True, null=True)
    reference_accession = models.CharField(max_length=100, blank=True, null=True)
    reference_phylum = models.CharField(max_length=100, blank=True, null=True)
    reference_order = models.CharField(max_length=100, blank=True, null=True)
    reference_genus = models.CharField(max_length=100, blank=True, null=True)
    reference_name = models.CharField(max_length=100, blank=True, null=True)

    checkm_marker_lineage = models.CharField(max_length=200, blank=True, null=True)
    checkm_genomes = models.IntegerField(blank=True, null=True)
    checkm_markers = models.IntegerField(blank=True, null=True)
    completeness = models.FloatField(blank=True, null=True)
    contamination = models.FloatField(blank=True, null=True)
    strain_heterogeneity = models.FloatField(blank=True, null=True)
    quality_score = models.FloatField(blank=True, null=True)

    gtdb_classification = models.TextField(blank=True, null=True)
    gtdb_phylum = models.CharField(max_length=200, blank=True, null=True)

    closest_genome_reference = models.CharField(max_length=200, blank=True, null=True)
    closest_genome_reference_radius = models.FloatField(blank=True, null=True)
    closest_genome_ani = models.FloatField(blank=True, null=True)
    closest_placement_reference = models.CharField(max_length=200, blank=True, null=True)

    classification_method = models.CharField(max_length=200, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    @property
    def symbiont_name(self):
        """
        Returns the symbiont name based on either reference_name or the species name from gtdb_classification.
        If neither is available, returns None.
        """
        # First try reference_name
        if self.reference_name and self.reference_name != "NA" and self.reference_name != "#N/A":
            return self.reference_name

        # Then try gtdb_classification
        if self.gtdb_classification and self.gtdb_classification != "NA" and self.gtdb_classification != "#N/A":
            try:
                # Split the classification string by semicolon
                taxa = [t.strip() for t in self.gtdb_classification.split(';') if t.strip()]
                if taxa:
                    last_taxon = taxa[-1]
                    # Remove any content within parentheses
                    if '(' in last_taxon:
                        last_taxon = last_taxon.split('(')[0].strip()
                    # If it's a species name (starts with s__), return the full name
                    if last_taxon.startswith('s__'):
                        return last_taxon[3:]  # Remove the s__ prefix for species
                    # For other taxonomic levels, keep the prefix
                    return last_taxon
            except Exception as e:
                print(f"Error processing GTDB classification for {self.genome_id}: {e}")
                print(f"GTDB classification: {self.gtdb_classification}")

        return None

    def __str__(self):
        name = self.symbiont_name
        if not name:
            name = self.genome_id
        host = f" - {self.host}" if self.host and self.host != "NA" and self.host != "#N/A" else ""
        return f"{name}{host}"

    class Meta:
        ordering = ['host', 'genome_id']
        indexes = [
            models.Index(fields=['host', 'genome_id']),
            models.Index(fields=['source_id']),
            models.Index(fields=['reference_phylum']),
            models.Index(fields=['gtdb_phylum']),
        ]