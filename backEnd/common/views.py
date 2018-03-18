from django.shortcuts import render

from django.conf import settings


def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "http://" + settings.CORS_ALLOW_HOST + ":3000"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = " * "
    response['Access-Control-Allow-Credentials'] = 'true'
    return response
