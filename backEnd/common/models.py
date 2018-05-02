# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    room_id = models.CharField(max_length=10, primary_key=True)  # 房间的id
    floor = models.IntegerField(null=False)  # 楼层数
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                default=None, related_name='ues_user')  # 使用当前房间的用户名
    pattern = models.BooleanField(null=False, default=0)  # 0表示被动模式，1表示主动模式
    status = models.IntegerField(null=False, default=0)  # 房间的状态，0表示无人，1表示有人
    people_counts = models.IntegerField(null=False, default=0)  # 房间内的人数
    expired_time = models.DateTimeField(null=True, blank=True)  # 主动模式下的到期时间
    last_nobody_time = models.DateTimeField(null=True, blank=True)  # 最近一次房内无人的时间

    class Meta:
        db_table = 'Room'

    def __str__(self):
        return str(self.room_id)


class Record(models.Model):
    id = models.AutoField(primary_key=True)  # 记录id，自动生成
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='user')  # 用户名
    room = models.ForeignKey('common.Room', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='room')  # 房间名
    current_status = models.IntegerField(null=False, default=0)  # 0表示未退房，1表示已退房
    create_date = models.DateTimeField(auto_now_add=True)  # 创建记录的时间
    check_in_date = models.DateTimeField(null=False)  # 登记入住的时间
    expired_date = models.DateTimeField(null=False)  # 到期时间
    check_out_date = models.DateTimeField()  # 退房时间

    class Meta:
        db_table = 'Record'

    def __str__(self):
        return str(self.id)
