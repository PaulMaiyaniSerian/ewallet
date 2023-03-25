from django.db import models

# Create your models here.

# c2b transactions
class C2BMpesaTransaction(models.Model):
    transactionType = models.CharField(max_length=200, blank=True)
    transID = models.CharField(max_length=200,blank=True)
    transTime = models.CharField(max_length=200, blank=True)
    transAmount = models.CharField(max_length=200, blank=True)
    businessShortCode = models.CharField(max_length=200, blank=True)
    billRefNumber = models.CharField(max_length=200, blank=True)
    invoiceNumber = models.CharField(max_length=200, blank=True)
    orgAccountBalance = models.CharField(max_length=200, blank=True)
    thirdPartyTransID = models.CharField(max_length=200, blank=True)
    mSISDN = models.CharField(max_length=200, blank=True)
    firstName = models.CharField(max_length=200, blank=True)
    middleName = models.CharField(max_length=200, blank=True)
    lastName = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"payment to account {self.billRefNumber}"
    

# lipa na mpesa transactions
class LNMTransactions(models.Model):
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
    merchantRequestID = models.CharField(max_length=200, blank=True)
    checkoutRequestID = models.CharField(max_length=200, blank=True)
    resultCode = models.CharField(max_length=200, blank=True)
    resultDesc = models.CharField(max_length=200, blank=True)
    amount = models.CharField(max_length=200, blank=True)
    mpesaReceiptNumber = models.CharField(max_length=200, blank=True)
    balance = models.CharField(max_length=200, blank=True)
    transactionDate = models.CharField(max_length=200, blank=True)
    phoneNumber = models.CharField(max_length=200, blank=True)
    target_account = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"payment to account {self.checkoutRequestID}"

