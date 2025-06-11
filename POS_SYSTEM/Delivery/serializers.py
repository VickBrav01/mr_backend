from .models import Delivery
from rest_framework import serializers

# from Payments.serializer import PaymentSerializer


class DeliverySerializer(serializers.ModelSerializer):
    # payments = PaymentSerializer(many=True, read)

    class Meta:
        model = Delivery
        fields = [
            "id",
            "parcel_id",
            "customer_name",
            "customer_phone",
            "delivery_address",
            "delivery_postal_code",
            "delivery_city",
            "delivery_status",
            "delivery_cost",
            "created_at",
            "delivered_at",
        ]

    