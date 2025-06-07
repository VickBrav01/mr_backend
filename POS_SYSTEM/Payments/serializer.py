from Delivery.models import Delivery
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "parcel_id",
            "customer_name",
            # "status",
            "delivery_cost",
            "delivered_at",
        ]
