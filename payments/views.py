from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# mpesa utils
from . import mpesa_utils

# models import
from .models import C2BMpesaTransaction, LNMTransactions
from accounts.models import UserWallet

# serializers
from .serializers import C2BMpesaTransactionSerializer


# Create your views here.
# endpoint for registering c2b callbacks
class RegisterMpesaCallBackUrlsView(APIView):

    def post(self, request):
        result = mpesa_utils.register_callbackurls()
        
        return Response(data=result, status=status.HTTP_200_OK)
    

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
        mpesa_transaction = C2BMpesaTransaction.objects.create(
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
        user_wallet.balance += float(mpesa_transaction.transAmount)
        user_wallet.save()


        return Response(status=status.HTTP_200_OK)


class C2BTransactionListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        # get all transacations that match the Userwallet from billrefnumber
        user_wallet = UserWallet.objects.get(user=request.user)
        transactions = C2BMpesaTransaction.objects.filter(billRefNumber=user_wallet.account_number)

        serializer = C2BMpesaTransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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



class StkPushWebHookApiView(APIView):
    # sample data
    '''
    {
        'Body': {
            'stkCallback': {
                'MerchantRequestID': '3786-9664944-1',
                'CheckoutRequestID': 'ws_CO_24032023165155703113953355', 
                'ResultCode': 0, 
                'ResultDesc': 'The service request is processed successfully.', 
                'CallbackMetadata': {
                    'Item': [
                        {'Name': 'Amount', 'Value': 1.0}, 
                        {'Name': 'MpesaReceiptNumber', 'Value': 'RCO4JCX8AW'}, 
                        {'Name': 'Balance'}, 
                        {'Name': 'TransactionDate', 'Value': 20230324165208}, 
                        {'Name': 'PhoneNumber', 'Value': 254113953355}]
                }
            }
        }
    }

    '''
    '''
    {
        'Body': {
            'stkCallback': {
                'MerchantRequestID': '39304-10030073-1', 
                'CheckoutRequestID': 'ws_CO_25032023065828577113953355', 
                'ResultCode': 1032, 
                'ResultDesc': 'Request cancelled by user'
                }
            }
        }
    '''

    def post(self, request):
        print(request.data, "stkpush webhook")
        data = request.data

        merchantRequestID = data["Body"]["stkCallback"]["MerchantRequestID"]
        checkoutRequestID = data["Body"]["stkCallback"]["CheckoutRequestID"]
        resultCode = data["Body"]["stkCallback"]["ResultCode"]
        resultDesc = data["Body"]["stkCallback"]["ResultDesc"]


        # use result code to check if cancelled or success
        # cancelled payment

        if resultCode == 1032:
            try:
                # get the transaction with merchid and checkoutid
                lnm_transaction = LNMTransactions.objects.get(
                    merchantRequestID=merchantRequestID,
                    checkoutRequestID=checkoutRequestID,
                )
                # update the trans
                lnm_transaction.resultCode = resultCode
                lnm_transaction.resultDesc = resultDesc
                lnm_transaction.save()

            except LNMTransactions.DoesNotExist:
                print("error data does not exist")

            
        elif resultCode == 0:
            # success payment
            merchantRequestID = data["Body"]["stkCallback"]["MerchantRequestID"]
            checkoutRequestID = data["Body"]["stkCallback"]["CheckoutRequestID"]
            resultCode = data["Body"]["stkCallback"]["ResultCode"]
            resultDesc = data["Body"]["stkCallback"]["ResultDesc"]

            amount = ""
            mpesaReceiptNumber = ""
            balance = ""
            transactionDate = ""
            phoneNumber = ""

            callbackMetadataItems = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            for item in callbackMetadataItems:
                if item["Name"] == "Amount":
                    amount = item["Value"]
                elif item["Name"] == "MpesaReceiptNumber":
                    mpesaReceiptNumber = item["Value"]
                elif item["Name"] == "Balance":
                    balance = ""
                elif item["Name"] == "TransactionDate":
                    transactionDate = item["Value"]
                elif item["Name"] == "PhoneNumber":
                    phoneNumber = item["Value"]
          
            # update transaction
            try:
                # get the transaction with merchid and checkoutid
                lnm_transaction = LNMTransactions.objects.get(
                    merchantRequestID=merchantRequestID,
                    checkoutRequestID=checkoutRequestID,
                )
                # update the trans
                lnm_transaction.resultCode = resultCode
                lnm_transaction.resultDesc = resultDesc
                lnm_transaction.amount = amount
                lnm_transaction.mpesaReceiptNumber = mpesaReceiptNumber
                lnm_transaction.balance = balance
                lnm_transaction.transactionDate = transactionDate
                lnm_transaction.phoneNumber = phoneNumber

                lnm_transaction.save()

                # get acccount from target_account in lnmTransaction
                user_wallet = UserWallet.objects.get(account_number=lnm_transaction.target_account)
                user_wallet.balance += float(lnm_transaction.amount)
                user_wallet.save()

            except LNMTransactions.DoesNotExist:
                print("error data does not exist")

        else:
            print("another result code received")


        return Response(status=status.HTTP_200_OK)



        
class StkPushProcessApiView(APIView):

    def post(self, request):
        # print(request.data)
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")
        number_to_pay_with = request.data.get("number_to_pay_with")

        if account_number and amount:

            result = mpesa_utils.stk_push(phone=number_to_pay_with, amount=amount, accountReference=account_number)

            # if it is successful store 

            return Response(data=result, status=status.HTTP_200_OK)

        else:
            message = {
                "error": "please provide the account number"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)