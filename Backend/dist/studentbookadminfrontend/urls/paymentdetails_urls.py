# studentbookadminfrontend/urls/paymentdetails_urls.py

from django.urls import path
from studentbookadminfrontend.views.paymentdetails_views import PaymentDetailsAPIView

urlpatterns = [
    path('', PaymentDetailsAPIView.as_view(), name='payment-details'),
]