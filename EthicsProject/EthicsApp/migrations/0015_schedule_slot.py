# Generated by Django 5.1.1 on 2024-11-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0014_remove_appointments_ethicalanswers_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='slot',
            field=models.CharField(max_length=25, null=True),
        ),
    ]