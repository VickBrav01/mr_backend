from rest_framework.generics import ListAPIView
from Delivery.models import Delivery
from .serializer import ReportSerializer
from rest_framework.permissions import IsAuthenticated


class ReportsListView(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
