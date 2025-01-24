from django.db import models

class Host(models.Model):
    """昆虫宿主模型"""
    species = models.CharField(max_length=200, unique=True, help_text="species")
    order = models.CharField(max_length=100, help_text="order")
    family = models.CharField(max_length=100, help_text="family")
    subfamily = models.CharField(max_length=100, null=True, blank=True, help_text="subfamily")
    genus = models.CharField(max_length=100, help_text="genus")
    common_name = models.CharField(max_length=200, blank=True, help_text="common name")
    description = models.TextField(blank=True, help_text="description text")
    figure_source = models.CharField(max_length=500, blank=True, null=True,
                                    help_text="Image source and license information")
    genome_id = models.CharField(max_length=20, blank=True, null=True,
                               help_text="Genome ID")
    genome_level = models.CharField(max_length=20, blank=True, null=True,
                                  help_text="Genome assembly level")
    busco = models.TextField(blank=True, null=True,
                           help_text="BUSCO assessment results")

    def __str__(self):
        return self.species

    class Meta:
        ordering = ['species']
        verbose_name_plural = "hosts"
