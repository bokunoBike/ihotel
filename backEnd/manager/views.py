# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
import time
from django.shortcuts import render
from django.http import HttpResponse

from .models import Room


def is_in_room(room_id):
    '''
    :param room_id: 房间号(string)
    :return:status :房间状态(int),0无人，1有人，2无此房间，3其他错误。
    '''
    try:
        result = Room.objects.filter(room_id=room_id)
        if not result.exists():  # 房间不存在
            status = 2
        else:
            status = result[0].status
    except Exception as e:
        # print(e)
        status = 3
    return status


@require_websocket
def get_room(request):
    room_id = request.GET.get('room_id', 0)
    room_status = is_in_room(room_id)
    while True:
        room_status = is_in_room(room_id)
        request.websocket.send(bytes(str(room_status), 'utf-8'))
        time.sleep(1)


@login_required
def home(request):
    room_id = request.GET.get('room_id', 0)
    room_status = is_in_room(room_id)
    return render(request, 'manager/home.html', {'room_id': room_id, 'room_status': room_status})
