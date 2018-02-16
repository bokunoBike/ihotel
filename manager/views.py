# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import RoomForm


def home(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        return render(request, 'manager/home.html', { 'room_id': room_id})
    else:  # 当正常访问时
        return render(request, 'manager/home.html', {})
