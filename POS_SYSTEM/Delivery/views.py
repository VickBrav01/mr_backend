from rest_framework.views import APIView
from rest_framework import status
from .models import Delivery
from .serializers import DeliverySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class ListAllDeliveries(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

class CreateDelivery(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer

    def post(self, request: Request, *args, **kwargs):
        try:
            data = request.data
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

class UpdateDelivery(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer

    def patch(self, request: Request, pk, *args, **kwargs):
        try:
            instance = get_object_or_404(Delivery, id=pk)  # Use id since parcel_id is not the PK
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Updated Delivery Successful",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred when updating the delivery",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteDelivery(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, pk):
        try:
            delivery = get_object_or_404(Delivery, id=pk)  # Use id since parcel_id is not the PK
            delivery.delete()
            return Response({"message": "Delivery deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e), "message": "An error occurred when deleting the delivery"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)