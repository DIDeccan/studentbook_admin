from django.urls import path
# from studentbookadminfrontend.views import ClassDistributionAPIView
from studentbookadminfrontend.views.dashboard_views import *
urlpatterns = [

    path('class-list',ClassListAPIView.as_view() ),
    path('student-list',StudentListAPIView.as_view()),
    path('class-distribution-pie-chart', ClassDistributionAPIView.as_view())

]