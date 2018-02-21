# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
import time
import json
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
    room_id = request.websocket.wait()
    room_status = is_in_room(room_id)
    while True:
        room_status = is_in_room(room_id)
        request.websocket.send(bytes(str(room_status), 'utf-8'))
        time.sleep(1)


def home(request):
    return render(request, 'manager/home.html', {'room_id': 0, 'room_status': 4})


@accept_websocket
def get_dbdata(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = "http方法"
            return HttpResponse(message)
        except:
            return render(request, 'manager/error.html')
    else:
        while True:
            db_query = Room.objects.all()
            message = [[l.room_id, l.status] for l in db_query]
            message = json.dumps(message)
            message = bytes(message, 'utf-8')
            # message = bytes(db_query[0].room_id, 'utf-8')
            request.websocket.send(message)
            time.sleep(1)


def show(request):
    db_query = Room.objects.all()
    return render(request, 'manager/show.html', {'db_query': db_query})
