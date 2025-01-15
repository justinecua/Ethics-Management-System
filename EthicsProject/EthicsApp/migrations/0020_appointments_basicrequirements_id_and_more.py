# Generated by Django 5.1.4 on 2025-01-14 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0019_alter_appointments_duration_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='basicRequirements_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.basicrequirements'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='supplementaryRequirements_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.supplementaryrequirements'),
        ),
    ]
