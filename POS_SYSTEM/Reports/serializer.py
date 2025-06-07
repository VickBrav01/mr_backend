from Delivery.models import Delivery
from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "id",
            "parcel_id",
            "customer_name",
            "delivery_address",
            "delivery_city",
            "created_at",
            "delivered_at",
        ]
