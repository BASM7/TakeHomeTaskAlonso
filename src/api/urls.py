from django.urls import path
from api import views

urlpatterns = [
    path('', views.process_payment, name='api_home'),
    path('api_logs/', views.APILogsView.as_view(), name='api_logs'),
    path('stripe_logs/', views.StripeLogsView.as_view(), name='stripe_logs'),
]
