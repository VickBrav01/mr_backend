from rest_framework.generics import ListAPIView
from Delivery.models import Delivery
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

class PaymentFilter(django_filters.FilterSet):
    is_paid = django_filters.BooleanFilter(field_name="is_paid")

    class Meta:
        model = Delivery
        fields = ["is_paid"]

class PaymentsListView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PaymentFilter
    search_fields = ["parcel_id", "customer_name"]
    ordering_fields = ["created_at", "customer_name"]
    ordering = ["-created_at"]