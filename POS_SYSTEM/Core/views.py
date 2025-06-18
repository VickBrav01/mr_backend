from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from Delivery.models import Delivery
from .serializers import DashboardStatsSerializer
from .models import BusinessDetails
from .serializers import BusinessDetailsSerializer

class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        try:
            instance = BusinessDetails.objects.first()
            if not instance:
                return Response(
                    {'message': 'No business details found', 'data': None},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = BusinessDetailsSerializer(instance)
            response = {
                'message': 'Retrieved Business Details Successfully',
                'data': serializer.data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'error': str(e),
                'message': 'An error occurred when retrieving business details',
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, *args, **kwargs):
        try:
            if BusinessDetails.objects.exists():
                return Response(
                    {'error': 'Business details already exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = BusinessDetailsSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response = {
                    'message': 'Created Business Details Successfully',
                    'data': BusinessDetailsSerializer(instance).data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'error': str(e),
                'message': 'An error occurred when creating business details',
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request: Request, *args, **kwargs):
        try:
            instance = BusinessDetails.objects.first()
            if not instance:
                return Response(
                    {'error': 'No business details found to update'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = BusinessDetailsSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                response = {
                    'message': 'Updated Business Details Successfully',
                    'data': BusinessDetailsSerializer(instance).data,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'error': str(e),
                'message': 'An error occurred when updating business details',
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DashboardStatsView(APIView):
    def get(self, request):
        stats = {
            'total_deliveries': Delivery.objects.count(),
            'total_customers': Delivery.objects.values('customer_name').distinct().count(),
            'total_payments': Delivery.objects.aggregate(Sum('delivery_cost'))['delivery_cost__sum'] or 0.00,
            'total_reports': Delivery.objects.count(),  # Using total deliveries as a proxy for reports
        }
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)