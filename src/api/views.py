from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from stripe.StripeManager import StripeManager
from .serializers import APILogSerializer, APIRequestSerializer, StripeLogSerializer
from api.models import PaymentRequest, PaymentResponse, StripeLog


@api_view(['POST'])
def process_payment(request):
    api_request_serializer = APIRequestSerializer(data=request.data)
    if api_request_serializer.is_valid():
        stripe_manager = StripeManager(request.data)
        return Response(stripe_manager.process_payment())
    else:
        return Response({'result': 'error', 'errors': payment_request_serializer.errors})


class APILogsView(GenericAPIView):
    queryset = PaymentRequest.objects.all()
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



