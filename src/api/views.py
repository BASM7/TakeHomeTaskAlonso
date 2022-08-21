from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from stripe.StripeManager import StripeManager
from .serializers import APILogSerializer, StripeLogSerializer
from api.models import APILog, StripeLog


@api_view(['POST'])
def process_payment(request):
    api_log_serializer = APILogSerializer(data={'data': request.data, 'log_type': 'request'})
    original_data = dict(request.data)
    if api_log_serializer.is_valid():
        api_log_serializer.save()

        stripe_manager = StripeManager(original_data)
        stripe_manager_response = stripe_manager.process_payment()

        api_log_serializer = APILogSerializer(data={'data': stripe_manager_response, 'log_type': 'response'})
        if api_log_serializer.is_valid():
            api_log_serializer.save()
        return Response(stripe_manager_response)
    else:
        error_response = {
            'result': 'failure',
            'transaction_id': 'Not executed',
            'errors': api_log_serializer.errors
        }
        api_log_serializer = APILogSerializer(data={'data': error_response, 'log_type': 'response'})
        if api_log_serializer.is_valid():
            api_log_serializer.save()


class APILogsView(GenericAPIView):
    queryset = APILog.objects.all()
    serializer_class = APILogSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(queryset=self.queryset)
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)


class StripeLogsView(GenericAPIView):
    queryset = StripeLog.objects.all()
    serializer_class = StripeLogSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(queryset=self.queryset)
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)



