# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from common.views import add_cors_headers, get_room_by_id, get_rooms_by_floor

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


@require_websocket
def get_room_signal(request):
    user = auth.get_user(request)
    room_id = request.GET.get('room_id')
    if user is None or not user.is_admin:  # 管理员未登录或非管理员
        room = None
    else:
        room = get_room_by_id('Z101')
    if room is None:  # 没有该房间
        room_data = {'signal1': [], 'signal2': []}
        data = json.dumps(room_data).encode()
        request.websocket.send(data)
    else:
        client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
        while True:
            current_time = datetime.datetime.now()
            over_time = current_time - datetime.timedelta(seconds=5)
            signal1 = []
            result = client.query("select mean(value) from %s WHERE sensor='num1' AND time <= %d AND time >= %d GROUP BY TIME(100ms);" % (
                room_id, current_time.timestamp() * 1000000000, over_time.timestamp() * 1000000000))
            for raw in result[room_id]:
                signal1.append(raw['mean'])
            signal2 = []
            result = client.query(
                "select mean(value) from %s WHERE sensor='num2' AND time <= %d AND time >= %d GROUP BY TIME(100ms);" % (
                    room_id, current_time.timestamp() * 1000000000, over_time.timestamp() * 1000000000))
            for raw in result[room_id]:
                signal2.append(raw['mean'])

            room_data = {'signal1': signal1, 'signal2': signal2}
            data = json.dumps(room_data).encode()
            request.websocket.send(data)
            time.sleep(5)


@require_websocket
def get_room_people_counts(request):  # 获取房间内的房间人数
    # print('start')
    user = auth.get_user(request)
    room_id = request.GET.get('room_id')
    if user is None or not user.is_admin:  # 管理员未登录或非管理员
        # print('not login')
        data = {"people_counts": 0}
        data = json.dumps(data).encode()
        request.websocket.send(data)
    else:
        room = get_room_by_id(room_id)
        if room is None:  # 没有该房间
            # print("The user doesn't use a room.")
            data = {"people_counts": 0}
            data = json.dumps(data).encode()
            request.websocket.send(data)
        else:
            # print('get it %s' % room.room_id)
            socket_status = 1
            while socket_status:
                room = get_room_by_id(room_id)
                people_counts = room.people_counts
                data = {"people_counts": people_counts}
                data = json.dumps(data).encode()
                # request.websocket.send(bytes(str(data), "utf-8"))
                request.websocket.send(data)
                time.sleep(1)
                # print(datetime.datetime.now())
                socket_status = request.websocket.read(1)
            # print('end')


@require_websocket
def get_room_people_counts_and_pattern(request):  # 获取房间内的房间人数
    # print('start')
    user = auth.get_user(request)
    room_id = request.GET.get('room_id')
    if user is None or not user.is_admin:  # 管理员未登录或非管理员
        # print('not login')
        data = {"people_counts": 0, "pattern": 0}
        data = json.dumps(data).encode()
        request.websocket.send(data)
    else:
        room = get_room_by_id(room_id)
        if room is None:  # 没有该房间
            # print("The user doesn't use a room.")
            data = {"people_counts": 0, "pattern": 0}
            data = json.dumps(data).encode()
            request.websocket.send(data)
        else:
            # print('get it %s' % room.room_id)
            socket_status = 1
            while socket_status:
                room = get_room_by_id(room_id)
                people_counts = room.people_counts
                pattern = room.pattern
                data = {"people_counts": people_counts, "pattern": pattern}
                data = json.dumps(data).encode()
                request.websocket.send(data)
                time.sleep(1)
                socket_status = request.websocket.read(1)
            # print('end')
