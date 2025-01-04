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

        # 移除开头和结尾的分隔符
        authors = self.authors.strip(";,")

        # 统一分隔符：先将逗号替换为分号，然后按分号分割
        authors_list = [author.strip() for author in authors.split(";") if author.strip()]

        # 如果第一次分割后列表为空，尝试用逗号分割
        if not authors_list:
            authors_list = [author.strip() for author in authors.split(",") if author.strip()]

        # 如果作者少于等于5个，直接返回全部，使用分号连接
        if len(authors_list) <= 5:
            return "; ".join(authors_list)

        # 对于超过5个作者的情况保持原有逻辑
        first_three = authors_list[:3]
        last_two = authors_list[-2:]
        return "; ".join(first_three) + " ... " + "; ".join(last_two)

    def __str__(self):
        return f"{self.id}: {self.title}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        db_table = 'article'
