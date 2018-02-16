# -*- coding: utf-8 -*-
from django import forms


class RoomForm(forms.Form):
    room_id = forms.IntegerField()
