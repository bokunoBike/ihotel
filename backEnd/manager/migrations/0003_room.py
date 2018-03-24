# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20180324_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('status', models.IntegerField()),
            ],
        ),
    ]
