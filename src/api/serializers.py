from rest_framework import serializers
from .models import StripeLog, APILog
from api.utils import mask_card_number, mask_card_cvv


class StripeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeLog
        fields = '__all__'


class APILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'

    def create(self, validated_data):
        instance = APILog(**validated_data)
        if 'card_number' in instance.data:
            instance.data['card_number'] = mask_card_number(instance.data['card_number'])
        if 'card_cvv' in instance.data:
            instance.data['card_cvv'] = mask_card_cvv(instance.data['card_cvv'])
        instance.save()
        return instance
