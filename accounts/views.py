# from django.shortcuts import render

# rest framework imports
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# serializer imports
from .serializers import RegisterSerializer

# model imports
from .models import UserWallet, User


# Create your views here.
class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # register user view
    def post(self, request):
        data = request.data

        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)