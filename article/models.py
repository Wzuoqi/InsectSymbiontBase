from django.db import models

class Article(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)  # 如果你需要自定义主键
    title = models.CharField(max_length=200, default="NA")
    authors = models.TextField(default="NA")
    publish_time = models.IntegerField(default=2024)
    journal = models.CharField(max_length=100, default="NA")
    doi = models.CharField(max_length=100, default="NA", unique=True)
    wos = models.CharField(max_length=100, default="NA")
    accession_numbers = models.TextField(default="NA")  # 用于存储多个序列号
    species = models.CharField(max_length=50, default="NA")


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
