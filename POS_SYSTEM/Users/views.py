from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import UserSerializer


# The `Register` class is an API view in Python that handles user registration by validating user
# input, creating a new user, and generating access tokens.
class Register(APIView):
    serializer_class = UserSerializer

    def post(self, request: Request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = {
                "message": "User Created",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The class `Login` is a subclass of `TokenObtainPairView` in Python.
class Login(TokenObtainPairView):
    pass
