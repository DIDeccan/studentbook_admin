from django.urls import path
from studentbookadminfrontend.views.dashboard_views import UserLoginListAPIView
from studentbookadminfrontend.views.dashboard_views import *
# from studentbookadminfrontend.views import LoginHistoryView
urlpatterns = [

    path('class_list',ClassListAPIView.as_view() ),
    path('student_list',StudentListAPIView.as_view()),
    path('class_distribution_pie_chart', ClassDistributionAPIView.as_view()),
    path('last_transactions', TransactionsAPIView.as_view()),
    path('user_login_details', UserLoginListAPIView.as_view()),
    # path('login-history', LoginHistoryView.as_view()),
    path('student_overview', StudentOverviewAPIView.as_view()),


]