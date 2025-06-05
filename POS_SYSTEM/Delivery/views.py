from rest_framework.views import APIView
from rest_framework import status
from .models import Delivery
from .serializer import DeliverySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ListAllDeliveries(ListAPIView):
    permission_class = [IsAuthenticated]
    serializers_class = DeliverySerializer
    queryset = Delivery.objects.all()


class UpdateDelivery(APIView):
    permission_class = [IsAuthenticated]
    serializers_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def patch(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        data = self.request.data
        try:
            instance = get_object_or_404(Delivery, pk=pk)
            serializer = self.serializers_class(
                data=data, instance=instance, partial=True
            )

            if serializer:
                serializer.save
                response = {
                    "message": "Updated Delivery Successful",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when updating the order",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateDelivery(APIView):
    permission_class = [IsAuthenticated]
    serializers_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def post(self, request: Request, *args, **kwargs):
        try:
            data = self.request.data
            serializer = self.serializers_class(data=data)
            if serializer:
                serializer.save
                response = {"message": "Delivery Made", "data": serializer.data}
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when creating the order",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
