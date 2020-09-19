"""HackNsu2_TEAM_RETURN_ZERO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from home import views as home_views
from login_signup import views as login_signup_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.index, name='home_page'),
    path('login', login_signup_views.login_view, name='login'),
    path('signup', login_signup_views.signup_view, name='signup'),
    path('logout', login_signup_views.logout_view, name='logout'),
    path('products', home_views.products, name='products'),
    path('vendors', home_views.vendors, name='vendors'),
    path('customers', home_views.customers, name='customers'),
    path('contact', home_views.contact, name='contact'),
]
