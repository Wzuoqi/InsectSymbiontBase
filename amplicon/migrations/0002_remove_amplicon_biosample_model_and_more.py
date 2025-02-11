# Generated by Django 4.2 on 2025-01-03 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplicon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amplicon',
            name='biosample_model',
        ),
        migrations.RemoveField(
            model_name='amplicon',
            name='isolation',
        ),
        migrations.RemoveField(
            model_name='amplicon',
            name='library_selection',
        ),
        migrations.RemoveField(
            model_name='amplicon',
            name='platform',
        ),
        migrations.AddField(
            model_name='amplicon',
            name='avg_spot_len',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='amplicon',
            name='bases',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='amplicon',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='amplicon',
            name='doi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='amplicon',
            name='host_family',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='amplicon',
            name='host_order',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='assay_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='bioproject',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='biosample',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='center_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='classification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='collection_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='env_broad_scale',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='env_local_scale',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='env_medium',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='geo_loc_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='geo_loc_name_country',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='geo_loc_name_country_continent',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='host',
            field=models.CharField(blank=True, db_index=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='host_sex',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='instrument',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amplicon',
            name='library_layout',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
