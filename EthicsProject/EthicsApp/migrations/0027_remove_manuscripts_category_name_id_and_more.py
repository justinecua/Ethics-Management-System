# Generated by Django 5.1.1 on 2025-01-16 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0026_merge_20250116_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manuscripts',
            name='category_name_id',
        ),
        migrations.RemoveField(
            model_name='manuscripts',
            name='type_of_study_id',
        ),
    ]
