# Generated by Django 5.1.1 on 2024-10-09 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0006_alter_schedule_schedule_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule_end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_start_time',
            field=models.TimeField(null=True),
        ),
    ]