# Generated by Django 4.2 on 2023-10-01 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('split', '0002_remove_splitsong_values_splitsong_album_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributionreportpayment',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]