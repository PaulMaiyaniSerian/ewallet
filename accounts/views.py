# from django.shortcuts import render

# rest framework imports
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# serializer imports
from .serializers import RegisterSerializer, UserWalletSerializer

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
        

# account balance endpoint
class UserWalletBalanceView(generics.GenericAPIView):
    serializer_class = UserWalletSerializer
    permission_classes = [IsAuthenticated]
    # register user view
    def get(self, request):
        # get logged in user
        user = request.user

        try:
            user_wallet = UserWallet.objects.get(user=user)
            serializer = UserWalletSerializer(user_wallet, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except UserWallet.DoesNotExist:
            message = {
                "error": "user_wallet for given user does not exist"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
            
       