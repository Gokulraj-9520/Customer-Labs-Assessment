from rest_framework import serializers
from .models import Account, Destination

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'account_id', 'account_name', 'app_secret_token', 'website']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'account', 'url', 'http_method', 'headers']
