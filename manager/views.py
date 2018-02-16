# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def home(request):
    tutorialList = ["HTML", "CSS", "iQuery", "Python", "Django"]
    return render(request, 'manager/home.html', {'tutorialList': tutorialList})
