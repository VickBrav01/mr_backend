# Generated by Django 5.2.1 on 2025-06-05 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_rename_businessdetails_businessmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BusinessModel',
            new_name='BusinessDetails',
        ),
    ]
