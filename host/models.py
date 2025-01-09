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
    

    def __str__(self):
        return self.species

    class Meta:
        ordering = ['species']
        verbose_name_plural = "hosts"
