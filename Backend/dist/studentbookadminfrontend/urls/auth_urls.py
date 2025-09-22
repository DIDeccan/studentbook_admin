# studentbookadminfrontend/urls/auth_urls.py

from django.urls import path
from studentbookadminfrontend.views.auth_views import *

urlpatterns = [
    # path('admin_login/', AdminLoginAPIView.as_view()),
    path('login', CustomTokenObtainPairView.as_view()),
    path('logout', LogoutView.as_view()),
 
]