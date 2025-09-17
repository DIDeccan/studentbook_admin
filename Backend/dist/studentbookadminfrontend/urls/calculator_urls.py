# studentbookadminfrontend/urls/calculator_urls.py

from django.urls import path
from studentbookadminfrontend.views.calculator_views import PriceCalculatorAPIView

urlpatterns = [
    path('calculate-price/', PriceCalculatorAPIView.as_view(), name='calculate-price'),
]