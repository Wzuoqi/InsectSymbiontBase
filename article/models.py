from django.db import models

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(default="NA")
    authors = models.TextField(default="NA")
    publish_time = models.IntegerField(default=2024)
    journal = models.TextField(default="NA")
    doi = models.CharField(max_length=200, default="NA")
    species = models.CharField(max_length=100, default="NA")
    symbiont = models.CharField(max_length=100, default="NA")

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        db_table = 'article'
