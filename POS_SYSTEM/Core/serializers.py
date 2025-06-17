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