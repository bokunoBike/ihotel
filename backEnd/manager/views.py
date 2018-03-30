# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from common.views import *

import time
import datetime
import json
from influxdb import InfluxDBClient


# @require_websocket
# def get_floor_info(request):  # 返回楼层中第一个房间的信号
#     user = auth.get_user(request)
#     floor = request.GET.get('floor', '0')
#     if user is None or not user.is_staff:  # 管理员未登录或非管理员
#         room_data = {'room_id': 0, 'signal' : 0}
#         data = json.dumps(room_data).encode()
#         request.websocket.send(data)
#     else:
#         try:
#             rooms = Room.objects.get(floor=floor)
#         except Room.DoesNotExist:
#             rooms = None
#         if rooms is None:  # 没有该楼层的房间
#             room_data = {'room_id': 0, 'signal': 0}
#             data = json.dumps(room_data).encode()
#             request.websocket.send(data)
#         else:
#             # print('get it')
#             while True:
#                 room_id = rooms[0].room_id
#                 room_data = {'room_id': 0, 'signal': 0}
#                 data = json.dumps(room_data).encode()
#                 # request.websocket.send(bytes(str(data), "utf-8"))
#                 request.websocket.send(data)
#                 time.sleep(1)

@require_websocket
def get_floor_rooms(request):
    user = auth.get_user(request)
    floor = int(request.GET.get('floor', '1'))
    if user is None or not user.is_admin:  # 管理员未登录或非管理员
        rooms = None
    else:
        rooms = get_rooms_by_floor(floor)
    if rooms is None:  # 没有该楼层的房间
        while True:
            room_data = {'room_counts': 0}
            data = json.dumps(room_data).encode()
            request.websocket.send(data)
            time.sleep(1)
    else:
        rooms_id =[]
        for room in rooms:
            rooms_id.append(room.room_id)
        client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
        while True:
            room_data = {}
            for room_id in rooms_id:
                signal = []
                result = client.query("select * from " + room_id + ";")
                for raw in result[room_id]:
                    signal.append((raw['time'], raw['sensor'], raw['value']))
                room_data[room_id] = signal
            data = json.dumps(room_data).encode()
            request.websocket.send(data)
            time.sleep(1)


@require_http_methods(["GET"])
def get_floor_rooms_id(request):
    user = auth.get_user(request)
    floor = int(request.GET.get('floor', '1'))
    rooms_id = []
    if user is None or not user.is_admin:  # 管理员未登录或非管理员
        pass
    else:
        rooms = get_rooms_by_floor(floor)
        for room in rooms:
            rooms_id.append(rooms_id)
    data = {"rooms_id": rooms_id}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response


@require_http_methods(["POST"])
def set_room_people_counts(request):  # 登录页面
    user = auth.get_user(request)
    room_id = request.POST.get('room_id')
    people_counts = int(request.POST.get('people_counts'))
    if people_counts < 0:
        people_counts = 0
    if user is None or not user.is_admin:  # 用户未登录或不为管理员
        data = {"result": 1}
    else:
        room = get_room_by_id(room_id)
        if room is None:  # 没有该房间
            data = {"result": 2}
        else:
            room.people_counts = people_counts
            room.save()
            data = {"result": 0}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response
