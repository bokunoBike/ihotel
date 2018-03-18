# -*- coding: utf-8 -*-
# 定义login app的url

from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^register', views.register, name="register"),
]