from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from rest_framework.authentication import TokenAuthentication

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
    )


User = get_user_model()

# Handle user Creation
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

# Handle Login
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = HTTP_200_OK)
        else:
            return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)    
    