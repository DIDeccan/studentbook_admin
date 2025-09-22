# studentbookadminfrontend/urls/calculator_urls.py

from django.urls import path
from studentbookadminfrontend.views.calculator_views import *

urlpatterns = [
    path('calculate_price/', PriceCalculatorAPIView.as_view()),
    path('classe_pricelist/', PriceCalculatorAPIView.as_view()),
]