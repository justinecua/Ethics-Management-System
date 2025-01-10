# Generated by Django 5.0.6 on 2024-10-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0004_remove_accounts_password_student_auth_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='description',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='schedname',
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
