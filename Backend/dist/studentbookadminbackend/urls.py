"""
URL configuration for studentbookadminbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# studentbook_admin/backend/urls.py (Your main project urls.py)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Dashboard URLs
    path('dashboard/', include('studentbookadminfrontend.urls.dashboard_urls')),

    # User Details URLs
    path('user_details/', include('studentbookadminfrontend.urls.userdetails_urls')),

    # Payment Details URLs
    path('payment_details/', include('studentbookadminfrontend.urls.paymentdetails_urls')),

    #content management URLS

    path('',include('studentbookadminfrontend.urls.content_management_urls')),

    #class URLS
    path("",include('studentbookadminfrontend.urls.class_urls')),

    #calculator URLS
    # path('', include('studentbookadminfrontend.urls.calculator_urls')),

    path('',include('studentbookadminfrontend.urls.auth_urls')),

    path("chaining/", include("smart_selects.urls"))


]

