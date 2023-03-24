from django.contrib import admin

# Register your models here.
from .models import MpesaTransaction

class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ["billRefNumber","transAmount"]


admin.site.register(MpesaTransaction, MpesaTransactionAdmin)