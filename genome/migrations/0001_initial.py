# Generated by Django 4.2 on 2025-01-31 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('genome_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('host', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('function', models.TextField(blank=True, null=True)),
                ('reference_accession', models.CharField(blank=True, max_length=100, null=True)),
                ('reference_phylum', models.CharField(blank=True, max_length=100, null=True)),
                ('reference_order', models.CharField(blank=True, max_length=100, null=True)),
                ('reference_genus', models.CharField(blank=True, max_length=100, null=True)),
                ('reference_name', models.CharField(blank=True, max_length=100, null=True)),
                ('checkm_marker_lineage', models.CharField(blank=True, max_length=200, null=True)),
                ('checkm_genomes', models.IntegerField(blank=True, null=True)),
                ('checkm_markers', models.IntegerField(blank=True, null=True)),
                ('completeness', models.FloatField(blank=True, null=True)),
                ('contamination', models.FloatField(blank=True, null=True)),
                ('strain_heterogeneity', models.FloatField(blank=True, null=True)),
                ('quality_score', models.FloatField(blank=True, null=True)),
                ('gtdb_classification', models.TextField(blank=True, null=True)),
                ('gtdb_phylum', models.CharField(blank=True, max_length=200, null=True)),
                ('closest_genome_reference', models.CharField(blank=True, max_length=200, null=True)),
                ('closest_genome_reference_radius', models.FloatField(blank=True, null=True)),
                ('closest_genome_ani', models.FloatField(blank=True, null=True)),
                ('closest_placement_reference', models.CharField(blank=True, max_length=200, null=True)),
                ('classification_method', models.CharField(blank=True, max_length=200, null=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['host', 'genome_id'],
            },
        ),
        migrations.AddIndex(
            model_name='genome',
            index=models.Index(fields=['host', 'genome_id'], name='genome_geno_host_87ea29_idx'),
        ),
        migrations.AddIndex(
            model_name='genome',
            index=models.Index(fields=['source_id'], name='genome_geno_source__f0aae7_idx'),
        ),
        migrations.AddIndex(
            model_name='genome',
            index=models.Index(fields=['reference_phylum'], name='genome_geno_referen_47ebcb_idx'),
        ),
        migrations.AddIndex(
            model_name='genome',
            index=models.Index(fields=['gtdb_phylum'], name='genome_geno_gtdb_ph_23962c_idx'),
        ),
    ]
