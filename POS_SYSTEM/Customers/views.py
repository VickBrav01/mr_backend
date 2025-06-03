from rest_framework.generics import ListAPIView
from .serializers import CustomerSerializer
from Delivery.models import Delivery
from rest_framework.permissions import IsAuthenticated


class ListCustomersView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
