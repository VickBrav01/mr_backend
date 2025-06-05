from django.db import models
from uuid import uuid4
from Customers.models import Customer

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

class Delivery(models.Model):
    parcel_id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=False)
    customer = models.ForeignKey(Customer,blank=True,null=True, on_delete=models.CASCADE, related_name="deliveries")
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_city = models.CharField(max_length=100, blank=True, null=True)
    delivery_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery to {self.customer.name} on {self.delivered_at.strftime('%Y-%m-%d %H:%M:%S') if self.delivered_at else 'Not Delivered'}"

    def get_delivery_address(self):
        return self.delivery_address or self.customer.address

    def get_delivery_postal_code(self):
        return self.delivery_postal_code or self.customer.postal_code

    def get_delivery_city(self):
        return self.delivery_city or self.customer.city