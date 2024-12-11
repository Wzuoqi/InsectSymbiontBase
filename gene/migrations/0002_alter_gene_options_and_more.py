# Generated by Django 4.2 on 2024-12-11 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gene',
            options={'ordering': ['genome_id', 'start_position']},
        ),
        migrations.RemoveIndex(
            model_name='gene',
            name='gene_gene_genome__7470c5_idx',
        ),
        migrations.RemoveField(
            model_name='gene',
            name='genome',
        ),
        migrations.AddField(
            model_name='gene',
            name='genome_id',
            field=models.CharField(db_index=True, max_length=100, null=True),
        ),
        migrations.AddIndex(
            model_name='gene',
            index=models.Index(fields=['genome_id', 'start_position'], name='gene_gene_genome__7470c5_idx'),
        ),
    ]
