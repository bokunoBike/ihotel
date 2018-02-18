# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket
from django.shortcuts import render
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


def home(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        room_status = is_in_room(room_id)
        return render(request, 'manager/home.html', {'room_id': room_id,
                                                     'room_status': room_status})
    else:  # 当正常访问时
        return render(request, 'manager/home.html', {'room_id': 0,
                                                     'room_status': 4})


@require_websocket
def get_dbdata(request):
    # db_query = Room.objects.all()
    # message = db_query[0].room_id
    message = "1"
    request.websocket.send(message)


def show(request):
    db_query = Room.objects.all()
    return render(request, 'manager/show.html', {'db_query': db_query})
