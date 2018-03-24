# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('current_status', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('check_in_date', models.DateTimeField()),
                ('expired_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'Record',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('floor', models.IntegerField()),
                ('pattern', models.BooleanField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('people_counts', models.IntegerField(default=0)),
                ('expired_time', models.DateTimeField(null=True, blank=True)),
                ('last_nobody_time', models.DateTimeField(null=True, blank=True)),
                ('user', models.OneToOneField(related_name='ues_user', null=True, on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Room',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='room',
            field=models.ForeignKey(related_name='room', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='common.Room', null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(related_name='userdetail', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
