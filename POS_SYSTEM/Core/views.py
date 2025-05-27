from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import BusinessDetailsSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .models import BusinessDetails

# Create your views here.


class BusinessDetailsView(APIView):
    queryset = BusinessDetails.objects.all()
    serializers_class = BusinessDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        business = get_object_or_404(self.queryset)
        try:
            serializer = self.serializers_class(instance=business)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValueError("Invalid serializer data")
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred while retrieving business details.",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, *args, **kwargs):
        data = self.request.data
        instance = get_object_or_404(self.queryset)
        try:
            serializer = self.serializers_class(
                instance=instance, data=data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValueError("Invalid serializer data")
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred while updating business details.",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
