# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import RoomForm


def home(request):
    if request.method == "POST":
        rlt = request.POST['room_id']
        return render(request, 'manager/home.html', {'rlt': rlt})
    else:  # 当正常访问时
        form = RoomForm()
        return render(request, 'manager/home.html', {'rlt': 'xas'})
