# Generated by Django 4.2 on 2023-10-01 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_distributionreport_numeric_columns_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DistributionReport',
        ),
    ]