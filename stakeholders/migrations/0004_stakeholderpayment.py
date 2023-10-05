# Generated by Django 4.2 on 2023-10-05 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('stakeholders', '0003_rename_artist_stakeholder'),
    ]

    operations = [
        migrations.CreateModel(
            name='StakeholderPayment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.transaction')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stakeholders.stakeholder')),
            ],
            bases=('accounts.transaction',),
        ),
    ]