from rest_framework import serializers
from .models import Delivery, MpesaTransaction

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = [
            "id",
            "delivery",
            "checkout_request_id",
            "phone_number",
            "amount",
            "status",
            "transaction_date",
            "mpesa_receipt_number",
            "result_code",
            "result_desc",
        ]

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "id",
            "parcel_id",
            "customer_name",
            "customer_phone",
            "delivery_address",
            "delivery_town",
            "delivery_route",
            "delivery_status",
            "delivery_cost",
            "created_at",
            "delivered_at",
            "is_paid",
        ]