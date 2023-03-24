from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# mpesa utils
from . import mpesa_utils

# models import
from .models import MpesaTransaction
from accounts.models import UserWallet

# serializers
from .serializers import MpesaTransactionSerializer


# Create your views here.
class C2BValidationView(APIView):

    def post(self, request):
        print(request.data, "validations")

        return Response(status=status.HTTP_200_OK)

class C2BConfirmationView(APIView):
    '''
    sample response
    {
        'TransactionType': 'Pay Bill', 
        'TransID': 'RCO41MKB14', 
        'TransTime': '20230324103853', 
        'TransAmount': '1.00', 
        'BusinessShortCode': '174379', 
        'BillRefNumber': '254113953355', 
        'InvoiceNumber': '', 
        'OrgAccountBalance': '943728.00', 
        'ThirdPartyTransID': '', 
        'MSISDN': 'bbff37cea44ac0b2d964ee0dfb8d2df8513dc7ba1b36129a929fc3fbd6dd4af4', 
        'FirstName': 'John', 
        'MiddleName': '', 
        'LastName': ''
        }
    '''

    def post(self, request):
        data = request.data
        print(data, "confirmation")
        
        # create the transaction
        mpesa_transaction = MpesaTransaction.objects.create(
            transactionType = request.data.get("TransactionType"),
            transID = request.data.get("TransID"),
            transTime = request.data.get("TransTime"),
            transAmount = request.data.get("TransAmount"),
            businessShortCode = request.data.get("BusinessShortCode"),
            billRefNumber = request.data.get("BillRefNumber"),
            invoiceNumber = request.data.get("InvoiceNumber"),
            orgAccountBalance = request.data.get("OrgAccountBalance"),
            thirdPartyTransID = request.data.get("ThirdPartyTransID"),
            mSISDN = request.data.get("MSISDN"),
            firstName = request.data.get("FirstName"),
            middleName = request.data.get("MiddleName"),
            lastName = request.data.get("LastName"),  
        )
        # update the user account balance from the billrefnumber
    
        try:
            user_wallet = UserWallet.objects.get(account_number=mpesa_transaction.billRefNumber)
        except UserWallet.DoesNotExist:
            message = {
                "error": "account with given number does not exist"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


        # add to balance
        user_wallet.balance += int(mpesa_transaction.transAmount)
        user_wallet.save()


        return Response(status=status.HTTP_200_OK)
    

class RegisterMpesaCallBackUrlsView(APIView):

    def post(self, request):
        result = mpesa_utils.register_callbackurls()
        
        return Response(data=result, status=status.HTTP_200_OK)


class SimulateC2BTransactionView(APIView):

    def post(self, request):
        # print(request.data)
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")

        if account_number and amount:

            result = mpesa_utils.simulate_c2b_transaction(account_number, amount)

            return Response(data=result, status=status.HTTP_200_OK)

        else:
            message = {
                "error": "please provide the account number"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StkPushApiView(APIView):

    def post(self, request):
        # print(request.data)
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")

        if account_number and amount:

            result = mpesa_utils.stk_push(account_number, amount)

            return Response(data=result, status=status.HTTP_200_OK)

        else:
            message = {
                "error": "please provide the account number"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StkPushWebHookView(APIView):

    def post(self, request):
        print(request.data, "stkpush webhook")

        return Response(status=status.HTTP_200_OK)


class TransactionListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        # get all transacations that match the Userwallet from billrefnumber
        user_wallet = UserWallet.objects.get(user=request.user)
        transactions = MpesaTransaction.objects.filter(billRefNumber=user_wallet.account_number)

        serializer = MpesaTransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
