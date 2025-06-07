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
    delivery_cost=models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    delivery_address = models.CharField(max_length=255)
    delivery_postal_code = models.CharField(max_length=20)
    delivery_city = models.CharField(max_length=100)
    delivery_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery to {self.customer_name} on {self.delivered_at.strftime('%Y-%m-%d %H:%M:%S')}"
