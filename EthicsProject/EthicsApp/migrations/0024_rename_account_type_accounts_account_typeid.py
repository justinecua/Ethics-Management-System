# Generated by Django 5.1.4 on 2025-01-15 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EthicsApp', '0023_rename_account_id_accounts_account_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='account_type',
            new_name='account_typeid',
        ),
    ]
