# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

app_name = 'manager'
urlpatterns = [
    url(r'^home', home, name="home"),
    url(r'^get_room', get_room),
]