from django.contrib import admin

# Register your models here.
from .models import UserWallet

class UserWalletAdmin(admin.ModelAdmin):
    list_display = ["user", "account_number", "balance"]

admin.site.register(UserWallet, UserWalletAdmin)