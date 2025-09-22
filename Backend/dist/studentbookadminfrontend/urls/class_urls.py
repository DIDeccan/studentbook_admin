from django.urls import path
from studentbookadminfrontend.views.class_views import *
 
urlpatterns = [

    path("classes_with_subjects/", ClassWIthSubjectsView.as_view()),
    path('calculate_price/', PriceCalculatorAPIView.as_view()),
    path('classe_pricelist/', PriceCalculatorAPIView.as_view()),
    
    ]