from rest_framework.generics import ListAPIView
from Delivery.models import Delivery
from .serializer import PaymentSerializer
from rest_framework.permissions import IsAuthenticated


class PaymentsListView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
