from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User


# add signals
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class UserWallet(models.Model):
    # one user can have only one wallet
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    # start balance with default of 0
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} account"
