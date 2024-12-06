# Generated by Django 4.2 on 2024-12-05 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symbiont', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='symbiont',
            name='localization',
        ),
        migrations.RemoveField(
            model_name='symbiont',
            name='transmission_mode',
        ),
        migrations.AddField(
            model_name='symbiont',
            name='function_tag',
            field=models.CharField(blank=True, default='NA', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='symbiont',
            name='journal',
            field=models.CharField(blank=True, default='NA', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='symbiont',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='symbiont',
            index=models.Index(fields=['symbiont_name'], name='symbiont_sy_symbion_8c61e1_idx'),
        ),
        migrations.AddIndex(
            model_name='symbiont',
            index=models.Index(fields=['year'], name='symbiont_sy_year_ae5952_idx'),
        ),
    ]