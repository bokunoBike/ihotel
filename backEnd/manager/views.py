# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from .models import Room

import time
import datetime
import json


@require_websocket
def get_floor_info(request):
    user = auth.get_user(request)
    floor = request.GET.get('floor', '0')
    room_data = []
    if user is None:  # 管理员未登录
        data = {"room_data": room_data, 'feedback': 'manager does not login'}
        data = json.dumps(data).encode()
        request.websocket.send(data)
    else:
        try:
            rooms = Room.objects.get(floor=floor)
        except Room.DoesNotExist:
            room = None
        if room is None:  # 没有该楼层的房间
            data = {"room_data": room_data,
                    'feedback': "The user doesn't use a room."}
            data = json.dumps(data).encode()
            request.websocket.send(data)
        else:
            # print('get it')
            while True:
                for i in rooms:
                    room_data.append(i.people_counts)
                data = {"room_data": room_data,
                        "feedback": "the people_counts"}
                data = json.dumps(data).encode()
                # request.websocket.send(bytes(str(data), "utf-8"))
                request.websocket.send(data)
                time.sleep(1)