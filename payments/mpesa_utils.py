import requests
from datetime import datetime
import base64

from django.conf import settings
from requests.auth import HTTPBasicAuth

def get_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    # print(response.text)

    access_token = response.json()["access_token"]


    return access_token


def register_callbackurls():
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

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



def stk_push(phone, amount):
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    businessShortCode = settings.SHORTCODE
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    transaction_type = "CustomerPayBillOnline"
    CallBackURL = settings.STKPUSH_CALLBACKURL

    # print(CallBackURL)
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = businessShortCode + passkey + timestamp

    
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    data = {
        "BusinessShortCode": businessShortCode,
        "Password": decode_password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type,
        "Amount": amount,
        "PartyA": phone,
        "PartyB": businessShortCode,
        "PhoneNumber": phone,
        "CallBackURL": CallBackURL,
        "AccountReference": "Paul Serian Shop backend",
        "TransactionDesc": "Payment to pauls shop"
    }
    # print(data)
    response = requests.post(url, json=data, headers=headers)
    # print(response.text)
    return response.json()


# function to simulate payment
def simulate_c2b_transaction(account_number, amount):
    # bill refnumber is target account to add the funds to
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

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
    


    # print(response.text)
    return response.json()


# simulate_c2b_transaction("254711393355", "12")'
