from django.db import models
from uuid import uuid4


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]


class Delivery(models.Model):
    parcel_id = models.UUIDField(
        default=uuid4, editable=False, unique=True, primary_key=False
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    delivery_address = models.CharField(max_length=255)
    delivery_postal_code = models.CharField(null=True, max_length=20)
    delivery_city = models.CharField(max_length=100)
    delivery_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )
    delivery_cost = models.DecimalField(decimal_places=2, default=0, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery to {self.customer_name} on {self.delivered_at.strftime('%Y-%m-%d %H:%M:%S')}"
