# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

app_name = 'manager'
urlpatterns = [
    url(r'^set_room_people_counts', set_room_people_counts, name="set_room_people_counts"),
    url(r'^get_floor_rooms', get_floor_rooms, name="get_floor_rooms"),
]
