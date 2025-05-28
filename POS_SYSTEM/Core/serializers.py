from .models import BusinessDetails
from rest_framework import serializers


class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetails
        fields = "__all__"
        read_only_fields = ["id"]
