# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

app_name = 'manager'
urlpatterns = [
    url(r'^home', home),
    url(r'^show', show),
    url(r'^get_dbdata', get_dbdata),
    url(r'^get_room', get_room),
]