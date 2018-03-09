# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=10, primary_key=True)  # 房间的id
    status = models.IntegerField()  # 房间的状态，0表示无人，1表示有人

    def __str__(self):
        return self.room_id
