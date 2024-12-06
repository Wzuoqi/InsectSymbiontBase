from django.db import models
from genome.models import Genome

class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    gene_id = models.CharField(max_length=100, unique=True, db_index=True)
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE, related_name='genes')

    locus_tag = models.CharField(max_length=100, blank=True, null=True)
    gene_name = models.CharField(max_length=100, blank=True, null=True)
    product = models.CharField(max_length=255)

    start_position = models.IntegerField()
    end_position = models.IntegerField()
    strand = models.CharField(max_length=1, choices=[('+', 'Forward'), ('-', 'Reverse')])

    sequence = models.TextField()

    function = models.TextField(blank=True, null=True)
    ec_number = models.CharField(max_length=50, blank=True, null=True)
    go_terms = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gene_id} - {self.gene_name or self.locus_tag}"

    class Meta:
        ordering = ['genome', 'start_position']
        indexes = [
            models.Index(fields=['genome', 'start_position']),
            models.Index(fields=['gene_name']),
            models.Index(fields=['locus_tag']),
        ]