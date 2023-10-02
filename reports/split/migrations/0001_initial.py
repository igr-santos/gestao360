# Generated by Django 4.2 on 2023-10-01 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stakeholders', '0002_alter_contact_kind'),
        ('reports', '0004_initial'),
        ('copyright', '0003_song_is_editor_alter_song_ecad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Split',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyright.song')),
            ],
        ),
        migrations.CreateModel(
            name='SplitSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', models.JSONField()),
                ('split', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='split.split')),
            ],
        ),
        migrations.CreateModel(
            name='SplitLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('artist', 'Artista principal'), ('feature', 'Participação Especial'), ('manager', 'Produtor Fonográfico')], max_length=30)),
                ('value', models.DecimalField(decimal_places=3, max_digits=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stakeholders.artist')),
                ('split', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='split.split')),
            ],
        ),
        migrations.CreateModel(
            name='DistributionReportPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.distributionreport')),
                ('split_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='split.splitsong')),
            ],
        ),
    ]
