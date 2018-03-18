# -*- coding: utf-8 -*-
# 定义视图，包括：设置主动模式下的时间，

import django.contrib.auth as auth
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from dwebsocket import require_websocket, accept_websocket

from common.models import Room
from common.views import add_cors_headers

import datetime
import time
import json


@require_http_methods(["POST"])
def set_expire_time(request):  # 登录页面
    user = auth.get_user(request)
    if user is None:  # 用户未登录
        data = {"set_expired_time_result": 2}
    else:
        hours = int(request.POST.get('hours'))
        if 0 <= int(hours) <= 2:  # 设置的时间在2小时之内
            minutes = int(request.POST.get('minutes'))
            seconds = int(request.POST.get('seconds'))
            current_time = datetime.datetime.now()
            expired_time = current_time + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            try:
                room = Room.objects.get(user=user)
            except Room.DoesNotExist:
                room = None
            if room is None:  # 该用户没有使用房间
                data = {"set_expired_time_result": 3}
            else:
                room.expired_time = expired_time
                room.pattern = True
                room.save()
                data = {"set_expired_time_result": 0}
        else:  # 设置的时间超出范围
            data = {"set_expired_time_result": 1}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response


def set_expire_time_test(request):
    return render(request, 'user/set_expire.html', {})


@require_http_methods(["GET"])
def get_expire_time(request):  # 登录页面
    user = auth.get_user(request)
    if user is None:  # 用户未登录
        data = {"expire_time": datetime.datetime.now(), 'feedback': 'user does not login'}
    else:
        try:
            room = Room.objects.get(user=user)
        except Room.DoesNotExist:
            room = None
        current_time = datetime.datetime.now()
        if room is None:  # 该用户没有使用房间
            data = {"expire_time": current_time, 'feedback': "The user doesn't use a room."}
        else:
            expired_time = room.expired_time
            expired_time = expired_time.replace(tzinfo=None)
            if expired_time is None or expired_time < current_time:
                data = {"expire_time": current_time,
                        'feedback': 'not set expire_time or has expired'}
            else:
                data = {"expire_time": expired_time, 'feedback': 'the expire time'}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response


# @require_http_methods(["GET"])
# def get_people_counts(request):  # 登录页面
#     user = auth.get_user(request)
#     if user is None:  # 用户未登录
#         data = {"people_counts": 0, 'feedback': 'user does not login'}
#     else:
#         try:
#             room = Room.objects.get(user=user)
#         except Room.DoesNotExist:
#             room = None
#         if room is None:  # 该用户没有使用房间
#             data = {"people_counts": 0, 'feedback': "The user doesn't use a room."}
#         else:
#             people_counts = room.people_counts
#             data = {"people_counts": people_counts, 'feedback': 'the people_counts'}
#     response = JsonResponse(data)
#     response = add_cors_headers(response)
#     return response

# @require_http_methods(["GET"])
@require_websocket
def get_room_info(request):  # 登录页面
    # print('start')
    user = auth.get_user(request)
    current_time = datetime.datetime.now()
    if user is None:  # 用户未登录
        # print('not login')
        data = {"people_counts": 0, "last_nobody_time": str(current_time), 'feedback': 'user does not login'}
        data = json.dumps(data).encode()
        request.websocket.send(data)
    else:
        try:
            room = Room.objects.get(user=user)
        except Room.DoesNotExist:
            room = None
        if room is None:  # 该用户没有使用房间
            # print('no using room')
            data = {"people_counts": 0, "last_nobody_time": str(current_time),
                    'feedback': "The user doesn't use a room."}
            data = json.dumps(data).encode()
            request.websocket.send(data)
        else:
            # print('get it')
            while True:
                people_counts = room.people_counts
                last_nobody_time = room.last_nobody_time
                if last_nobody_time is None:
                    last_nobody_time = current_time
                data = {"people_counts": people_counts, "last_nobody_time": str(last_nobody_time),
                        "feedback": "the people_counts"}
                data = json.dumps(data).encode()
                # request.websocket.send(bytes(str(data), "utf-8"))
                request.websocket.send(data)
                time.sleep(1)
