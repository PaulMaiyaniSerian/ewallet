from . import constants
import requests

from requests.auth import HTTPBasicAuth

def get_access_token():
    consumer_key = constants.CONSUMER_KEY
    consumer_secret = constants.CONSUMER_SECRET

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
    print(response.text)

    access_token = response.json()["access_token"]


    return access_token


def register_callbackurls():
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "ShortCode": constants.SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": constants.CONFIRMATIONURL,
        "ValidationURL": constants.VALIDATIONURL,
    }

    response = requests.post(url, json=data, headers=headers, verify=False )

    print(response.text)

# get_access_token()
# register_callbackurls()


def simulate_c2b_transaction():
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "ShortCode": constants.SHORTCODE,
        "CommandID": "CustomerPayBillOnline",
        "Amount": "1",
        "Msisdn": constants.TESTMSISDN,
        "BillRefNumber": "254113953355"

    }

    response = requests.post(url, json=data, headers=headers)

    print(response.text)


# simulate_c2b_transaction()