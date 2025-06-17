from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Delivery.models import Delivery
from Delivery.serializers import DeliverySerializer

class GlobalSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'results': []}, status=status.HTTP_200_OK)

        delivery_qs = Delivery.objects.filter(
            Q(parcel_id__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query) |
            Q(delivery_city__icontains=query) |
            Q(delivery_address__icontains=query)
        )[:10]
        delivery_results = DeliverySerializer(delivery_qs, many=True).data
        delivery_results = [{'type': 'Delivery', **result} for result in delivery_results]

        return Response({'results': delivery_results}, status=status.HTTP_200_OK)