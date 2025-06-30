from rest_framework.views import APIView
from rest_framework import status
from .models import Delivery, MpesaTransaction
from .serializers import DeliverySerializer, MpesaTransactionSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FilterClasses
from django.shortcuts import get_object_or_404
from Notification.services import in_transit_message
from .services import MpesaService
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ListAllDeliveries(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = FilterClasses
    search_fields = ["customer_name", "delivery_town", "created_at"]
    ordering_fields = ["created_at", "customer_name"]
    ordering = ["-created_at"]

class RetrieveUpdateDelivery(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def get(self, request: Request, *args, **kwargs):
        try:
            pk = self.kwargs.get("pk")
            delivery = get_object_or_404(Delivery, pk=pk)
            serializer = self.serializer_class(delivery)
            response = {
                "message": "Retrieved Delivery Successfully",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when retrieving the delivery",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        data = request.data
        try:
            instance = get_object_or_404(Delivery, pk=pk)
            serializer = self.serializer_class(
                instance=instance, data=data, partial=True
            )
            if serializer.is_valid():
                delivery = serializer.save()
                new_status = delivery.delivery_status
                if new_status == "in_transit":
                    in_transit_message(delivery)
                response = {
                    "message": "Updated Delivery Successfully",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when updating the order",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, *args, **kwargs):
        try:
            pk = self.kwargs.get("pk")
            delivery = get_object_or_404(Delivery, pk=pk)
            delivery.delete()
            return Response(
                {"message": "Deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateDelivery(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def post(self, request: Request, *args, **kwargs):
        try:
            data = request.data.copy()
            # Map delivery_city to delivery_town
            if 'delivery_city' in data:
                data['delivery_town'] = data.pop('delivery_city')
            # Map delivery_postal_code to delivery_town if needed
            if 'delivery_postal_code' in data:
                data['delivery_town'] = data.get('delivery_town', data['delivery_postal_code'])
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Delivery Created",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when creating the delivery",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InitiateMpesaPayment(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MpesaTransactionSerializer

    def post(self, request: Request, *args, **kwargs):
        try:
            pk = self.kwargs.get("pk")
            delivery = get_object_or_404(Delivery, pk=pk)
            
            # Check if delivery is already paid
            if delivery.is_paid:
                return Response(
                    {"error": "This delivery is already paid"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate delivery cost
            if not delivery.delivery_cost or delivery.delivery_cost <= 0:
                return Response(
                    {"error": "Delivery cost must be greater than zero"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Initialize M-Pesa service
            mpesa_service = MpesaService()
            callback_url = settings.MPESA_CALLBACK_URL  # Ensure this is set in settings.py
            account_reference = f"DEL-{delivery.parcel_id}"
            transaction_desc = f"Payment for delivery {delivery.parcel_id}"

            # Initiate STK Push
            response = mpesa_service.stk_push(
                phone_number=delivery.customer_phone,
                amount=str(delivery.delivery_cost),
                account_reference=account_reference,
                transaction_desc=transaction_desc,
                callback_url=callback_url
            )

            # Create MpesaTransaction record
            transaction = MpesaTransaction.objects.create(
                delivery=delivery,
                checkout_request_id=response.get('CheckoutRequestID'),
                phone_number=delivery.customer_phone,
                amount=delivery.delivery_cost,
                status="initiated"
            )
            serializer = self.serializer_class(transaction)

            return Response(
                {
                    "message": "M-Pesa STK Push initiated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error initiating M-Pesa payment: {str(e)}")
            return Response(
                {
                    "error": str(e),
                    "message": "An error occurred while initiating payment"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )