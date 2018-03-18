# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-12 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20180312_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_nobody_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='pattern',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='people_counts',
            field=models.IntegerField(default=0),
        ),
    ]
