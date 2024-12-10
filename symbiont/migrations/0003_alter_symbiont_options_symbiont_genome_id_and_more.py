# Generated by Django 4.2 on 2024-12-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symbiont', '0002_remove_symbiont_localization_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='symbiont',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='symbiont',
            name='genome_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='symbiont',
            name='host_order',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='symbiont',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='symbiont',
            name='record_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
