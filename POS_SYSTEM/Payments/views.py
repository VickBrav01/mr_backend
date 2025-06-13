from rest_framework.generics import ListAPIView
from Delivery.models import Delivery
from .serializer import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class PaymentsListView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["created_at"]
    search_fields = ["parcel_id", "customer_name", "email"]
    ordering_fields = ["created_at", "username"]
    ordering = ["-created_at"]
