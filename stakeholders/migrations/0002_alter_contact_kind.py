# Generated by Django 4.2 on 2023-09-17 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stakeholders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='kind',
            field=models.CharField(choices=[('phone', 'Telefone'), ('email', 'Email')], max_length=20),
        ),
    ]
