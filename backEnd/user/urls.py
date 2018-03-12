# -*- coding: utf-8 -*-
# 定义user app的url

from django.conf.urls import url
from . import views


app_name = 'user'
urlpatterns = [
    url(r'^set_expire_time', views.set_expire_time, name="set_expire_time"),
    url(r'^get_expire_time', views.get_expire_time, name="get_expire_time"),
    url(r'^test_set_expire_time', views.set_expire_time_test, name="test_set_expire_time"),
]
