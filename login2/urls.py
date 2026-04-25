"""
URL configuration for login2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from login import views as login_views
from django.shortcuts import redirect
from solicitud import views as solicitud_views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('login/', login_views.login_view, name='login'),
    path('home/', login_views.home, name='home'),
    path('logout', login_views.logout_view, name='logout'),
    path('solicitud/', solicitud_views.solicitud_producto, name='solicitud_producto'),
    path('register/', login_views.register_view, name='register'),
]
