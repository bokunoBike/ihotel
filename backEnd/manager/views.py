# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.shortcuts import render
from django.http import HttpResponse

from .models import Room

import time
import datetime
import json


@require_websocket
def get_floor_info(request):  # 返回楼层中第一个房间的信号
    user = auth.get_user(request)
    floor = request.GET.get('floor', '0')
    if user is None or not user.is_staff:  # 管理员未登录或非管理员
        room_data = {'room_id': 0, 'signal' : 0}
        data = json.dumps(room_data).encode()
        request.websocket.send(data)
    else:
        try:
            rooms = Room.objects.get(floor=floor)
        except Room.DoesNotExist:
            rooms = None
        if rooms is None:  # 没有该楼层的房间
            room_data = {'room_id': 0, 'signal': 0}
            data = json.dumps(room_data).encode()
            request.websocket.send(data)
        else:
            # print('get it')
            while True:
                room_id = rooms[0].room_id
                room_data = {'room_id': 0, 'signal': 0}
                data = json.dumps(room_data).encode()
                # request.websocket.send(bytes(str(data), "utf-8"))
                request.websocket.send(data)
                time.sleep(1)