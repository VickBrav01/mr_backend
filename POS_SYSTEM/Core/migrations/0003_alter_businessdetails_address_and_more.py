# Generated by Django 5.2.1 on 2025-05-27 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0002_businessdetails_delete_businesscoredetails"),
    ]

    operations = [
        migrations.AlterField(
            model_name="businessdetails",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="businessdetails",
            name="name2",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
