# Generated by Django 5.1.1 on 2024-11-25 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0012_alter_student_mobile_number_alter_student_receipt_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThesisType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ThesisType', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='receipt_no2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='appointments',
            name='thesis_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.thesistype'),
        ),
    ]
