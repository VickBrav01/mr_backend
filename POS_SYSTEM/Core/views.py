from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BusinessDetails
from .serializers import BusinessDetailsSerializer


class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        try:
            business = BusinessDetails.objects.first()
            if not business:
                return Response({"detail": "No business found."}, status=204)

            serializer = BusinessDetailsSerializer(business)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request: Request, *args, **kwargs):
        instance = BusinessDetails.objects.first()
        if instance:
            data = self.request.data
            serializer = BusinessDetailsSerializer(instance, data=data, partial=True)
        else:
            serializer = BusinessDetailsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
