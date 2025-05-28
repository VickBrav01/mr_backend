from rest_fraework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import UserSerializer


class UserRegistrationView(APIView):
    def post(self, request: Request, *args, **kwargs):
        data = self.request.data
        serializer = UserSerializer(data=data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response = {
                    "message": "User Created",
                    "data": serializer.data,
                    
                }

                return Response(data=response, status=status.HTTP_201_CREATED)
            raise ValueError("Invalid serializer data")
        except Exception as e:
            response = {
                "error": str(e),
                "message": "An error occurred while registering the user.",
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(TokenObtainPairView):
    pass


