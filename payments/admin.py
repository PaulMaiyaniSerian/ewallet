from django.contrib import admin

# Register your models here.
from .models import C2BMpesaTransaction, LNMTransactions

class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "billRefNumber",
        "transAmount",
        "transID", 
        "transTime", 
        "firstName" 
    ]


admin.site.register(C2BMpesaTransaction, MpesaTransactionAdmin)

class LNMTransactionsAdmin(admin.ModelAdmin):
    list_display = [
        "checkoutRequestID", 
        "merchantRequestID", 
        "amount",
        "phoneNumber",
        "transactionDate", 
        "mpesaReceiptNumber",
        "resultDesc",
        "target_account"
    ]

admin.site.register(LNMTransactions, LNMTransactionsAdmin)