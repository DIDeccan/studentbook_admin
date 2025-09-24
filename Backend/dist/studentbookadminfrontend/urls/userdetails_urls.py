# studentbookadminfrontend/urls/userdetails_urls.py

from django.urls import path
from studentbookadminfrontend.views.userdetails_views import (
    UserDetailsAPIView,
    EditUserAPIView,
    SuspendUserAPIView,
    DeleteUserAPIView,
    ResetPasswordAPIView,
    VerifyAndUpdatePhoneAPIView   # <-- Add this line
)

urlpatterns = [
    path('', UserDetailsAPIView.as_view()),
    path('edit/<int:pk>/', EditUserAPIView.as_view()),
    path('suspend/<int:pk>/', SuspendUserAPIView.as_view()),
    path('delete/<int:pk>/', DeleteUserAPIView.as_view()),
    path('reset-password/<int:pk>/', ResetPasswordAPIView.as_view()),
    # New URLs for OTP verification
    # path('send-otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify-phone/<int:pk>/', VerifyAndUpdatePhoneAPIView.as_view(), name='verify-phone'),
]



