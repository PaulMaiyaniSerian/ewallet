from rest_framework import serializers
from .models import User, UserWallet
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(
        write_only=True,
        required=True,
        )

    class Meta:
        model = User
        fields = ( 'username', 'password', 'password2', "phone")
        extra_kwargs = {
            'password': {'required': True},
            'password2': {'required': True},
            'phone': {'required': True}
        }
        ref_name = "Register Normal User"

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # check if there is a phone number in accounts
        try:
            userwallet = UserWallet.objects.get(account_number=attrs["phone"])
            # if userwallet exists raise a validation error
            if userwallet:
                raise serializers.ValidationError({"phone": "phone number already used use another number"})
        except UserWallet.DoesNotExist:
            # if it does not exist allow user creation to proceed
            pass

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        # print(validated_data)

        # create Userwallet after user is saved 
        UserWallet.objects.create(
            user=user,
            account_number=validated_data["phone"]
        )

        return user