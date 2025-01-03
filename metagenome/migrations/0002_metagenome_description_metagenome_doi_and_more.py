# Generated by Django 4.2 on 2025-01-03 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metagenome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metagenome',
            name='description',
            field=models.CharField(default='None', max_length=2000),
        ),
        migrations.AddField(
            model_name='metagenome',
            name='doi',
            field=models.CharField(db_index=True, default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='metagenome',
            name='host_family',
            field=models.CharField(db_index=True, default='NA', max_length=200),
        ),
        migrations.AddField(
            model_name='metagenome',
            name='host_order',
            field=models.CharField(db_index=True, default='NA', max_length=200),
        ),
    ]
