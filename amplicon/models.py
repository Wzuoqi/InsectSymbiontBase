from django.db import models

# Create your models here.

class Amplicon(models.Model):
    id = models.AutoField(primary_key=True)
    run = models.CharField(max_length=100, unique=True, db_index=True)
    assay_type = models.CharField(max_length=100, null=True, blank=True)
    biosample = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    bytes = models.BigIntegerField(null=True, blank=True)

    # 测序平台信息
    center_name = models.CharField(max_length=500, null=True, blank=True)
    instrument = models.CharField(max_length=200, null=True, blank=True)
    library_layout = models.CharField(max_length=50, null=True, blank=True)
    avg_spot_len = models.CharField(max_length=20, null=True, blank=True)
    bases = models.BigIntegerField(null=True, blank=True)

    # 项目信息
    bioproject = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    classification = models.CharField(max_length=200, null=True, blank=True)

    # 地理信息
    geo_loc_name_country = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    geo_loc_name_country_continent = models.CharField(max_length=200, null=True, blank=True)
    collection_date = models.CharField(max_length=100, null=True, blank=True)
    geo_loc_name = models.CharField(max_length=500, null=True, blank=True)
    lat_lon = models.CharField(max_length=200, null=True, blank=True)

    # 宿主信息
    host = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    host_order = models.CharField(max_length=200, null=True, blank=True)
    host_family = models.CharField(max_length=200, null=True, blank=True)

    # 环境信息
    env_broad_scale = models.CharField(max_length=500, null=True, blank=True)
    env_local_scale = models.CharField(max_length=500, null=True, blank=True)
    env_medium = models.CharField(max_length=500, null=True, blank=True)
    host_sex = models.CharField(max_length=50, null=True, blank=True)

    # 描述信息
    description = models.TextField(null=True, blank=True)
    doi = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.run} - {self.host} ({self.geo_loc_name_country})"

    class Meta:
        ordering = ['run', 'geo_loc_name_country', 'host', 'collection_date']
        indexes = [
            models.Index(fields=['run', 'geo_loc_name_country', 'host', 'collection_date']),
        ]
