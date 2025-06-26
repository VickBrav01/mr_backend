from django.db import models
from uuid import uuid4


def generate_parcel_id():
    return str(uuid4()).replace("-", "")[:8].upper()


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

ROUTES_CHOICES = (
    ("Langata", "Langata"),
    ("Ngong", "Ngong"),
    ("Jogoo", "Jogoo"),
    ("Mombasa", "Mombasa"),
    ("Thika", "Thika"),
    ("Waiyaki", "Waiyaki"),
    ("Kiambu", "Kiambu"),
    ("Limuru", "Limuru"),
    ("Ardhwings_Kodek", "Ardhwings Kodek"),
    ("Lower_Kabete", "Lower Kabete"),
    ("Peponi", "Peponi"),
)


class Delivery(models.Model):
    parcel_id = models.CharField(
        max_length=6, default=generate_parcel_id, unique=True, editable=False
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    delivery_address = models.CharField(max_length=255)
    delivery_route = models.CharField(
        max_length=50, choices=ROUTES_CHOICES, default=None
    )
    delivery_town = models.CharField(max_length=100)
    delivery_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "parcel_id",
                    "customer_name",
                    "customer_phone",
                    "delivery_town",
                    "delivery_address",
                ]
            ),
        ]

    def __str__(self):
        return f"Delivery {self.parcel_id} to {self.customer_name}"
