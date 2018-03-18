# -*- coding: utf-8 -*-
# 定义user app的url

from django.conf.urls import url
from . import views


app_name = 'user'
urlpatterns = [
    url(r'^set_expire_time', views.set_expire_time, name="set_expire_time"),
    url(r'^get_expire_time', views.get_expire_time, name="get_expire_time"),
    url(r'^get_room_info', views.get_room_info, name="get_room_info")
]
