# Generated by Django 4.2 on 2023-10-01 14:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributionreport',
            name='numeric_columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='distributionreport',
            name='columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), blank=True, null=True, size=None),
        ),
    ]
