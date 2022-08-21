from django.contrib import admin
from api.models import APILog, StripeLog


class APILogAdmin(admin.ModelAdmin):
    pass


class StripeLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(APILog, APILogAdmin)
admin.site.register(StripeLog, StripeLogAdmin)
