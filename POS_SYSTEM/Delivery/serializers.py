from rest_framework import serializers
from .models import Delivery
from Customers.models import Customer

class DeliverySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True)

    class Meta:
        model = Delivery
        fields = [
            "id",
            "parcel_id",
            "customer",
            "delivery_address",
            "delivery_postal_code",
            "delivery_city",
            "delivery_status",
            "created_at",
            "delivered_at",
        ]

    def to_representation(self, instance):
        # Include nested customer data in the response
        representation = super().to_representation(instance)
        if instance.customer:
            representation["customer"] = {
                "id": instance.customer.id,
                "name": instance.customer.name,
                "phone": instance.customer.phone,
                "address": instance.customer.address,
                "postal_code": instance.customer.postal_code,
                "city": instance.customer.city,
            }
        return representation