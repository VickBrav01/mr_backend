from Delivery.models import Delivery
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    # Paid status include afterwards
    class Meta:
        model = Delivery
        fields = [
            "parcel_id",
            "customer_name",
            "delivery_status",
            "delivery_cost",
            "delivered_at",
        ]
