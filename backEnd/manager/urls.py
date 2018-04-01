# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

app_name = 'manager'
urlpatterns = [
    url(r'set_room_people_counts', set_room_people_counts, name="set_room_people_counts"),
    url(r'get_room_signal', get_room_signal, name="get_room_signal"),
    url(r'get_floor_rooms_id', get_floor_rooms_id, name="get_floor_rooms_id"),
    url(r'get_room_people_counts_and_pattern', get_room_people_counts_and_pattern, name="get_room_people_counts_and_pattern"),
    url(r'get_room_people_counts', get_room_people_counts, name="get_room_people_counts"),
    url(r'test_signal', test_signal, name="test_signal"),
]
