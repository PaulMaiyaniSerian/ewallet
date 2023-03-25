from rest_framework import serializers

from .models import C2BMpesaTransaction

class C2BMpesaTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = C2BMpesaTransaction
        fields = "__all__"