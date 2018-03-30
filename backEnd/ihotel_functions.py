from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, JsonResponse

from .models import Room


def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "http://" + settings.CORS_ALLOW_HOST + ":3000"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = " * "
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def get_available_rooms(request):
    available_rooms = []
    try:
        rooms = Room.objects.get(user=None)
    except Room.DoesNotExist:
        rooms = []
    for room in rooms:
        available_rooms.append(room.room_id)
    data = {"available_rooms": available_rooms}
    response = add_cors_headers(JsonResponse(data))
    return response


def get_room_by_id(room_id):
    try:
        room = Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        room = None
    return room


def get_rooms_by_floor(floor):
    try:
        rooms = Room.objects.get(floor=floor)
    except Room.DoesNotExist:
        rooms = None
    return rooms