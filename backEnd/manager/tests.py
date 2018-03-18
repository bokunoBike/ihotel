# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import is_in_room
from .models import *


class TestIs_in_room(TestCase):
    def test_is_in_room(self):
        # 测试is_in_room函数
        # 测试的内容包括：
        #   ①房间内无人
        #   ②房间内有人
        #   ③无此房间
        #   ④其他情况
        Room.objects.create(room_id="Z101", status=0)
        Room.objects.create(room_id="Z102", status=1)
        self.assertEqual(is_in_room("Z101"), 0)  # ①
        self.assertEqual(is_in_room("Z102"), 1)  # ②
        self.assertEqual(is_in_room("F101"), 2)  # ③
