# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dwebsocket import require_websocket, accept_websocket
from django.contrib.auth.decorators import login_required
import time
from django.shortcuts import render
from django.http import HttpResponse

from .models import Room


@require_websocket
def get_room(request):
    room_id = request.GET.get('room_id', 0)
    room_status = is_in_room(room_id)
    while True:
        room_status = is_in_room(room_id)
        request.websocket.send(bytes(str(room_status), 'utf-8'))
        time.sleep(1)

