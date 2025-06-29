from rest_framework.generics import ListAPIView
from Delivery.models import Delivery
from .serializer import ReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters


class ReportsListView(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["parcel_id", "customer_name"]
    ordering_fields = ["created_at", "customer_name"]
    ordering = ["-created_at"]