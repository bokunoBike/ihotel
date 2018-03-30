# -*- coding: utf-8 -*-
# 定义common app的url

from django.conf.urls import url
from . import views

app_name = 'common'
urlpatterns = [
    url(r'^get_available_rooms', views.get_available_rooms, name="get_available_rooms"),
]