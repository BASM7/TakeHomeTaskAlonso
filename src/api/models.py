from django.db import models


class PaymentRequest(models.Model):
    card_number = models.CharField(max_length=16)
    card_expiry_month = models.CharField(max_length=2)
    card_expiry_year = models.CharField(max_length=4)
    card_cvv = models.CharField(max_length=3)
    amount_in_cents = models.TextField()


class PaymentResponse(models.Model):
    transaction_id = models.TextField()
    result = models.CharField(max_length=10)
    errors = models.TextField()


class APIRequest(models.Model):
    card_number = models.CharField(max_length=16)
    card_expiry_month = models.CharField(max_length=2)
    card_expiry_year = models.CharField(max_length=4)
    card_cvv = models.CharField(max_length=3)
    amount_in_cents = models.TextField()


class APILog(models.Model):
    data = models.JSONField()
    log_type = models.CharField(max_length=10, default='request')


class StripeLog(models.Model):
    data = models.JSONField()
    log_type = models.CharField(max_length=10, default='request')

