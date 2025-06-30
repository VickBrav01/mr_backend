from rest_framework import serializers
from Delivery.models import Delivery

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "parcel_id",
            "customer_name",
            "delivery_status",
            "delivery_cost",
            "delivered_at",
            "is_paid",
        ]