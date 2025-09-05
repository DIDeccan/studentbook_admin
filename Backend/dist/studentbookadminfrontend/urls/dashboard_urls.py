from django.urls import path
from studentbookadminfrontend.views.dashboard_views import UserLoginListAPIView
from studentbookadminfrontend.views.dashboard_views import *
# from studentbookadminfrontend.views import LoginHistoryView
urlpatterns = [

    path('class-list',ClassListAPIView.as_view() ),
    path('student-list',StudentListAPIView.as_view()),
    path('class-distribution-pie-chart', ClassDistributionAPIView.as_view()),
    path('last-transactions', TransactionsAPIView.as_view()),
    path('user-login-details', UserLoginListAPIView.as_view()),
    # path('login-history', LoginHistoryView.as_view()),

    


]