# Generated by Django 4.2 on 2025-01-31 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(db_index=True, default='None', max_length=200)),
                ('source_id', models.CharField(db_index=True, max_length=200)),
                ('gene_id', models.CharField(db_index=True, max_length=200)),
                ('nr_id', models.CharField(blank=True, max_length=200, null=True)),
                ('identity', models.FloatField(blank=True, default=0.0, null=True)),
                ('alignment_length', models.IntegerField(blank=True, default=0, null=True)),
                ('mismatches', models.IntegerField(blank=True, default=0, null=True)),
                ('gap_openings', models.IntegerField(blank=True, default=0, null=True)),
                ('query_start', models.IntegerField(blank=True, default=0, null=True)),
                ('query_end', models.IntegerField(blank=True, default=0, null=True)),
                ('subject_start', models.IntegerField(blank=True, default=0, null=True)),
                ('subject_end', models.IntegerField(blank=True, default=0, null=True)),
                ('evalue', models.FloatField(blank=True, default=0.0, null=True)),
                ('bit_score', models.FloatField(blank=True, default=0.0, null=True)),
                ('sequence', models.TextField(default='')),
                ('gene_length', models.IntegerField(default=0)),
                ('nr_annotation', models.TextField(blank=True, default='', null=True)),
                ('nr_species', models.TextField(blank=True, default='', null=True)),
                ('seed_ortholog', models.TextField(blank=True, default='', null=True)),
                ('eggnog_evalue', models.FloatField(blank=True, default=0.0, null=True)),
                ('eggnog_score', models.FloatField(blank=True, default=0.0, null=True)),
                ('eggnog_ogs', models.TextField(blank=True, default='', null=True)),
                ('max_annot_lvl', models.TextField(blank=True, default='', null=True)),
                ('cog_category', models.TextField(blank=True, default='', null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('preferred_name', models.TextField(blank=True, default='', null=True)),
                ('go_terms', models.TextField(blank=True, default='', null=True)),
                ('ec_number', models.TextField(blank=True, default='', null=True)),
                ('kegg_ko', models.TextField(blank=True, default='', null=True)),
                ('kegg_pathway', models.TextField(blank=True, default='', null=True)),
                ('kegg_module', models.TextField(blank=True, default='', null=True)),
                ('kegg_reaction', models.TextField(blank=True, default='', null=True)),
                ('kegg_rclass', models.TextField(blank=True, default='', null=True)),
                ('brite', models.TextField(blank=True, default='', null=True)),
                ('kegg_tc', models.TextField(blank=True, default='', null=True)),
                ('cazy', models.TextField(blank=True, default='', null=True)),
                ('bigg_reaction', models.TextField(blank=True, default='', null=True)),
                ('pfams', models.TextField(blank=True, default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='gene',
            index=models.Index(fields=['source_id'], name='gene_gene_source__01c406_idx'),
        ),
        migrations.AddIndex(
            model_name='gene',
            index=models.Index(fields=['nr_id'], name='custom_nr_id_idx'),
        ),
        migrations.AddIndex(
            model_name='gene',
            index=models.Index(fields=['nr_species'], name='gene_gene_nr_spec_3f68e6_idx'),
        ),
        migrations.AddIndex(
            model_name='gene',
            index=models.Index(fields=['cog_category'], name='gene_gene_cog_cat_228691_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='gene',
            unique_together={('source_id', 'gene_id')},
        ),
    ]
