"""site2 URL Configuration

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
from . import views

urlpatterns = [
    path('',views.vote),
    path('login/',views.login),
    path('logout/',views.logout),
    path('check_login/',views.check_login),
    path('make_vote/',views.make_vote),
    path('max_page/',views.max_page),
    path('get_table/',views.get_table),
    path('vote_exist/',views.vote_exist),
    path('test/',views.test),
    path('select/',views.select),
    path('get_my_vote/',views.get_my_vote),

    
]