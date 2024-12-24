# Generated by Django 4.2 on 2024-12-24 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(help_text='物种学名', max_length=200, unique=True)),
                ('order', models.CharField(help_text='目', max_length=100)),
                ('family', models.CharField(help_text='科', max_length=100)),
                ('subfamily', models.CharField(blank=True, help_text='亚科', max_length=100, null=True)),
                ('genus', models.CharField(help_text='属', max_length=100)),
                ('common_name', models.CharField(blank=True, help_text='俗名', max_length=200)),
                ('description', models.TextField(blank=True, help_text='描述信息')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'hosts',
                'ordering': ['species'],
            },
        ),
    ]
