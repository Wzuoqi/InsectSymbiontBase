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

    @property
    def formatted_authors(self):
        if self.authors in ["NA", "", None]:
            return "NA"

        # 确定分隔符
        separator = ";" if ";" in self.authors else ","
        authors_list = [author.strip() for author in self.authors.split(separator)]

        # 如果作者少于等于5个，直接返回全部
        if len(authors_list) <= 5:
            return separator + " ".join(authors_list)

        # 获取前三个和最后两个作者
        first_three = authors_list[:3]
        last_two = authors_list[-2:]

        # 组合结果
        return f"{separator} ".join(first_three) + " ... " + f"{separator} ".join(last_two)

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        db_table = 'article'
