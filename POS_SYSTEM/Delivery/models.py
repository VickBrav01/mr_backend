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
        max_length=8, default=generate_parcel_id, unique=True, editable=False
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
    is_paid = models.BooleanField(default=False)  # Track payment status

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

class MpesaTransaction(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="mpesa_transactions")
    checkout_request_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("initiated", "Initiated"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled"),
        ],
        default="initiated"
    )
    transaction_date = models.DateTimeField(auto_now_add=True)
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    result_code = models.CharField(max_length=10, null=True, blank=True)
    result_desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"M-Pesa Transaction {self.checkout_request_id} for Delivery {self.delivery.parcel_id}"