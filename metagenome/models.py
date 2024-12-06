from django.db import models

# Create your models here.

class Metagenome(models.Model):
    id = models.AutoField(primary_key=True)
    run = models.CharField(max_length=100, unique=True, db_index=True)
    assay_type = models.CharField(max_length=100, default="NA")
    biosample = models.CharField(max_length=100, db_index=True)
    bytes = models.BigIntegerField(null=True, blank=True)
    center_name = models.CharField(max_length=200)
    instrument = models.CharField(max_length=100)
    library_layout = models.CharField(max_length=50)
    library_selection = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    bioproject = models.CharField(max_length=100, db_index=True)

    geo_loc_name_country = models.CharField(max_length=100, db_index=True)
    geo_loc_name_country_continent = models.CharField(max_length=100)
    collection_date = models.CharField(max_length=100, db_index=True,default="NA")
    geo_loc_name = models.CharField(max_length=200)
    biosample_model = models.CharField(max_length=100)
    lat_lon = models.CharField(max_length=100, null=True, blank=True)

    host = models.CharField(max_length=200, db_index=True)
    isolation = models.CharField(max_length=200, db_index=True, default="NA")

    def __str__(self):
        return f"{self.run} - {self.host} ({self.geo_loc_name_country})"

    class Meta:
        ordering = ['run', 'geo_loc_name_country', 'host', 'collection_date']
        indexes = [
            models.Index(fields=['run', 'geo_loc_name_country', 'host', 'collection_date']),
        ]
