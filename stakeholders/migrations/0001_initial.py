# Generated by Django 4.2 on 2023-09-17 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=180)),
                ('artist_name', models.CharField(max_length=100)),
                ('related_artist', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('kind', models.CharField(choices=[('phone', 'Phone'), ('email', 'Email')], max_length=20)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContactCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stakeholders.artist')),
                ('contacts', models.ManyToManyField(to='stakeholders.contact')),
            ],
        ),
    ]
