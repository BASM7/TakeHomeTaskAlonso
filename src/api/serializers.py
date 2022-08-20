from rest_framework import serializers
from .models import PaymentRequest, PaymentResponse, StripeLog, APILog, APIRequest


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ('card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvv', 'amount_in_cents')


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentResponse
        fields = ('transaction_id', 'result', 'errors')


class StripeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeLog
        fields = '__all__'


class APILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'


class APIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequest
        fields = '__all__'
