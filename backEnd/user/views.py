# -*- coding: utf-8 -*-
# 定义视图，包括：设置主动模式下的时间，

import django.contrib.auth as auth
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from dwebsocket import require_websocket, accept_websocket

from common.models import Room, Record
from common.views import add_cors_headers, get_room_by_user, get_room_by_id

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
        # print(hours)
        if 0 <= int(hours) <= 2:  # 设置的时间在2小时之内
            minutes = int(request.POST.get('minutes'))
            seconds = int(request.POST.get('seconds'))
            # print(minutes)
            # print(seconds)
            current_time = datetime.datetime.now()
            expired_time = current_time + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            room = get_room_by_user(user)
            if room is None:  # 该用户没有使用房间
                data = {"set_expired_time_result": 3}
            else:
                room.expired_time = expired_time
                room.pattern = True
                room.save()
                # print(user.username)
                # print(room.room_id)
                data = {"set_expired_time_result": 0}
        else:  # 设置的时间超出范围
            data = {"set_expired_time_result": 1}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response


@require_http_methods(["GET"])
def get_expire_time(request):  # 登录页面
    # print('start')
    user = auth.get_user(request)
    if user is None:  # 用户未登录
        data = {"expire_time": datetime.datetime.now(), 'feedback': 'user does not login'}
    else:
        room = get_room_by_user(user)
        current_time = datetime.datetime.now()
        if room is None:  # 该用户没有使用房间
            data = {"expire_time": current_time, 'feedback': "The user doesn't use a room."}
        else:
            expired_time = room.expired_time
            if expired_time is None:
                expired_time = current_time
            expired_time = expired_time.replace(tzinfo=None)
            # print(current_time)
            # print(expired_time)
            if expired_time <= current_time:
                data = {"expire_time": current_time,
                        'feedback': 'not set expire_time or has expired'}
            else:
                data = {"expire_time": expired_time, 'feedback': 'the expire time'}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response


@require_websocket
def get_room_info(request):  # 返回房间人数
    # print('start')
    user = auth.get_user(request)
    # print(user.username)
    if user is None:  # 用户未登录
        # print('not login')
        data = {"people_counts": 0}
        data = json.dumps(data).encode()
        request.websocket.send(data)
    else:
        room = get_room_by_user(user)
        if room is None:  # 该用户没有使用房间
            # print("The user doesn't use a room.")
            data = {"people_counts": 0}
            data = json.dumps(data).encode()
            request.websocket.send(data)
        else:
            # print('get it %s' % room.room_id)
            socket_status = 1
            while socket_status:
                room = Room.objects.get(user=user)
                people_counts = room.people_counts
                data = {"people_counts": people_counts}
                data = json.dumps(data).encode()
                # request.websocket.send(bytes(str(data), "utf-8"))
                request.websocket.send(data)
                time.sleep(1)
                # print(datetime.datetime.now())
                socket_status = request.websocket.read(1)
                # print('end')


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False


@require_http_methods(["POST"])
def create_record(request):
    user = auth.get_user(request)
    check_in_date_str = request.POST.get('check_in_time')
    days = int(request.POST.get('days'))
    if is_valid_date(check_in_date_str):
        check_in_date = datetime.datetime(check_in_date_str)
        expired_time = check_in_date + datetime.timedelta(days=days)
    else:
        expired_time = None
    room_id = request.POST.get('room_id')
    room = get_room_by_id(room_id)

    if user is None:  # 用户未登录
        data = {"result": 0, "message": "用户未登录"}
    elif room is None:  # 房间不存在
        data = {"result": 0, "message": "房间不存在"}
    elif room.user is not None:
        data = {"result": 0, "message": "房间已经被预定"}
    elif expired_time is None:
        data = {"result": 0, "message": "时间错误"}
    else:
        record = Record(user=user, room=room, check_in_date=check_in_date,
                        expired_time=expired_time, current_status=0,
                        create_record=datetime.datetime.now())
        record.save()
        data = {"result": 1, "message": "预定成功"}
    response = JsonResponse(data)
    response = add_cors_headers(response)
    return response
