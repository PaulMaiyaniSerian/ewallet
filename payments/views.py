from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# mpesa utils
from . import mpesa_utils


# Create your views here.
class C2BValidationView(APIView):

    def post(self, request):
        print(request.data, "validations")

        return Response(status=status.HTTP_200_OK)

class C2BConfirmationView(APIView):

    def post(self, request):
        print(request.data, "confirmation")

        return Response(status=status.HTTP_200_OK)