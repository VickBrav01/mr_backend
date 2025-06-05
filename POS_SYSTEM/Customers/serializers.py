from Delivery.models import Delivery
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "customer_name",
            "customer_phone",
            "delivery_address",
            "delivery_status",
            "delivered_at",
        ]
