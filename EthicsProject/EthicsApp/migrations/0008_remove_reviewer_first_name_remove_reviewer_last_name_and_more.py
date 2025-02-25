# Generated by Django 5.1.1 on 2024-10-11 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0007_alter_schedule_schedule_end_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='reviewer',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='reviewer',
            name='smc_email',
        ),
        migrations.AddField(
            model_name='reviewer',
            name='auth_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='smc_id_no',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
