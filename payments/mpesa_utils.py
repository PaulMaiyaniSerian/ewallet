import requests
from datetime import datetime
import base64
from requests.auth import HTTPBasicAuth

from django.conf import settings
from .models import LNMTransactions

def get_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET

    url = settings.MPESA_AUTH_URL
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    access_token = response.json()["access_token"]
    return access_token


def register_callbackurls():
    access_token = get_access_token()

    url = settings.MPESA_REGISTER_CALLBACK_URL
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "ShortCode": settings.SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": settings.CONFIRMATIONURL,
        "ValidationURL": settings.VALIDATIONURL,
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()



def stk_push(phone, amount, accountReference):
    url = settings.PROCESS_STKPUSH_URL
    businessShortCode = settings.SHORTCODE
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    transaction_type = "CustomerPayBillOnline"
    CallBackURL = settings.STKPUSH_CALLBACKURL
    passkey = settings.PASSKEY
    data_to_encode = businessShortCode + passkey + timestamp

    
    online_password = base64.b64encode(data_to_encode.encode())
    decoded_password = online_password.decode('utf-8')

    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    data = {
        "BusinessShortCode": businessShortCode,
        "Password": decoded_password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type,
        "Amount": amount,
        "PartyA": phone,
        "PartyB": businessShortCode,
        "PhoneNumber": phone,
        "CallBackURL": CallBackURL,
        "AccountReference": accountReference,
        "TransactionDesc": "Payment to Swallet"
    }
    # sample response
    # {
    #     "MerchantRequestID": "39323-10048461-1",
    #     "CheckoutRequestID": "ws_CO_25032023071038568113953355",
    #     "ResponseCode": "0",
    #     "ResponseDescription": "Success. Request accepted for processing",
    #     "CustomerMessage": "Success. Request accepted for processing"
    # }


    response = requests.post(url, json=data, headers=headers).json()

    '''
    if response code == 0 then it is succesful and we can add 
    merchant id and checkout id plus target_account
    to the transactions which will later be modified in callback hook
    '''

    print(response)
    if response.get("ResponseCode") == "0":
        print("successfuly sent")
        LNMTransactions.objects.create(
            merchantRequestID=response["MerchantRequestID"],
            checkoutRequestID=response["CheckoutRequestID"],
            target_account=accountReference
        )

    return response


# function to simulate payment
def simulate_c2b_transaction(account_number, amount):
    # bill refnumber is target account to add the funds to
    access_token = get_access_token()

    url = settings.C2B_SIMULATE_URL

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "ShortCode": settings.SHORTCODE,
        "CommandID": "CustomerPayBillOnline",
        "Amount": amount,
        "Msisdn": settings.TESTMSISDN,
        "BillRefNumber": account_number
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()


# simulate_c2b_transaction("254711393355", "12")'
