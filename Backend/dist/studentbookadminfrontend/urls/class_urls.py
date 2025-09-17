from django.urls import path
from studentbookadminfrontend.views.class_views import *
 
urlpatterns = [

    path("classes_with_subjects/", ClassWIthSubjectsView.as_view()),
    
    ]