from rest_framework import serializers
from .models import BusinessDetails
import cloudinary

class BusinessDetailsSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(use_url=True, required=False, allow_null=True)

    class Meta:
        model = BusinessDetails
        fields = ['id', 'name', 'pin', 'address', 'phone', 'email', 'logo']
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.logo:
            data['logo'] = cloudinary.utils.cloudinary_url(instance.logo.public_id, secure=True)[0]
        return data
    


class DashboardStatsSerializer(serializers.Serializer):
    total_deliveries = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_reports = serializers.IntegerField()