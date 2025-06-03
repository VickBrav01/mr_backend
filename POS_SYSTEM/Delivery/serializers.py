from .models import Delivery
from rest_framework import serializers


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = "__all__"
