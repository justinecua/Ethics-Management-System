# Generated by Django 5.1.1 on 2024-10-26 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0010_schedule_account_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(null=True)),
                ('appointment_name', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('institution', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasicRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basicRequirements', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthicalRiskAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethicalAnswers', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthicalRiskQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethicalQuestions', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupplementaryRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplementaryRequirements', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfStudy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_study', models.CharField(max_length=350, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Apointments',
        ),
        migrations.RemoveField(
            model_name='manuscripts',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='manuscripts',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='manuscripts',
            name='type_of_study',
        ),
        migrations.AddField(
            model_name='manuscripts',
            name='category_name_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='manuscripts',
            name='type_of_study_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='manuscript_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.manuscripts'),
        ),
        migrations.AddField(
            model_name='student',
            name='manuscript_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.manuscripts'),
        ),
        migrations.AlterField(
            model_name='manuscripts',
            name='no_studyparticipants',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='manuscripts',
            name='study_site',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='manuscripts',
            name='thesis_description',
            field=models.TextField(max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='manuscripts',
            name='thesis_title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='appointments',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.student'),
        ),
        migrations.AddField(
            model_name='ethicalriskanswers',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.student'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='ethicalAnswers_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.ethicalriskanswers'),
        ),
        migrations.AddField(
            model_name='ethicalriskanswers',
            name='ethicalQuestions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EthicsApp.ethicalriskquestions'),
        ),
    ]
