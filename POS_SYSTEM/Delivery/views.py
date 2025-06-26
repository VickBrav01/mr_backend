from rest_framework.views import APIView
from rest_framework import status
from .models import Delivery
from .serializers import DeliverySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FilterClasses
from django.shortcuts import get_object_or_404
from Notification.services import (
    in_transit_message,
    # delivered_message,
    # canceled_message,
)


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
    search_fields = ["customer_name", "email", "created_at"]
    ordering_fields = ["created_at", "username"]
    ordering = ["-created_at"]


class RetrieveUpdateDelivery(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def get(self, request: Request, *args, **kwargs):
        """
        Retrieves a single Delivery instance by its primary key.
        """
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
        """
        Partially updates a Delivery instance.
        Triggers status-specific messages if the delivery status changes.
        """
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
                # elif new_status == "delivered":
                #     delivered_message(delivery)
                # elif new_status == "cancelled":
                #     canceled_message(delivery)
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
        """
        Deletes a Delivery instance.
        Sends a cancellation message before deletion.
        """
        try:
            pk = self.kwargs.get("pk")
            delivery = get_object_or_404(Delivery, pk=pk)
            # canceled_message(delivery)
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
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Delivery Made",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when creating the order",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
