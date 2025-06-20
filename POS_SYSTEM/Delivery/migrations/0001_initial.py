# Generated by Django 5.2.1 on 2025-06-18 14:32

import Delivery.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parcel_id', models.CharField(default=Delivery.models.generate_parcel_id, editable=False, max_length=6, unique=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_phone', models.CharField(max_length=15)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('delivery_address', models.CharField(max_length=255)),
                ('delivery_postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('delivery_city', models.CharField(max_length=100)),
                ('delivery_status', models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['parcel_id', 'customer_name', 'customer_phone', 'delivery_city', 'delivery_address'], name='Delivery_de_parcel__71ede4_idx')],
            },
        ),
    ]
