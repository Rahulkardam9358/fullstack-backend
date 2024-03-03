from authentication.models import User, Address
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.ReadOnlyField()
    class Meta:
        model = User
        exclude = ['password']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']