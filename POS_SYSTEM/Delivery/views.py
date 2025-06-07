from rest_framework.views import APIView
from rest_framework import status
from .models import Delivery
from .serializers import DeliverySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from Notification.services import (
    in_transit_message,
    delivered_message,
    canceled_message,
)


class ListAllDeliveries(ListAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()


class UpdateDelivery(APIView):
    permission_class = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def patch(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        data = self.request.data
        try:
            instance = get_object_or_404(Delivery, pk=pk)
            old_status = instance.delivery_status  # Track old status

            serializer = self.serializer_class(
                instance=instance, data=data, partial=True
            )
            if serializer.is_valid():
                updated_instance = serializer.save()  # FIXED: actually save it
                new_status = updated_instance.delivery_status

                # Send SMS based on new status
                if new_status == "In Transit":
                    in_transit_message(updated_instance)
                elif new_status == "delivered":
                    delivered_message(updated_instance)
                elif new_status == "cancelled":
                    canceled_message(updated_instance)

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
            if not delivery:
                return Response(
                    {"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST
                )
            canceled_message(delivery)
            delivery.delete()
            return Response(
                {"message": "Deleted successful"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateDelivery(APIView):
    permission_class = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def post(self, request: Request, *args, **kwargs):
        try:
            data = self.request.data
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
