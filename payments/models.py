from django.db import models

# Create your models here.
class MpesaTransaction(models.Model):
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
