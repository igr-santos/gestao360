# Generated by Django 4.2 on 2023-10-01 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0003_delete_distributionreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='reports/datafiles/')),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('columns', models.JSONField(blank=True, null=True)),
                ('dtypes', models.JSONField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
