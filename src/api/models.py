from django.db import models


class APILog(models.Model):
    data = models.JSONField()
    log_type = models.CharField(max_length=10, default='request')


class StripeLog(models.Model):
    data = models.JSONField()
    log_type = models.CharField(max_length=10, default='request')

    def __str__(self):
        return self.log_type

