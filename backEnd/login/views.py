# -*- coding: utf-8 -*-
# 定义视图，包括：主页视图、登录视图、注销视图、注册视图

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .admin import UserCreateForm
from .forms import LoginForm
from .models import User
from common.views import add_cors_headers


@require_http_methods(["POST"])
def login(request):  # 登录页面
    username = request.POST.get('roomNumber')
    password = request.POST.get('thePassword')

    user = auth.authenticate(request, username=username, password=password)
    if user is not None:  # 登录成功
        auth.login(request, user)
        if user.is_admin:  # 管理员登录
            data = {"login_result": 0}
            response = JsonResponse(data)
            response = add_cors_headers(response)
            return response
        else:  # 普通用户登录
            data = {"login_result": 1}
            response = JsonResponse(data)
            response = add_cors_headers(response)
            return response
    else:  # 登录失败
        data = {"login_result": 2}
        response = JsonResponse(data)
        response = add_cors_headers(response)
        return response


def logout(request):
    auth.logout(request)  # 注销用户
    return redirect(reverse('login:home'))


def register(request):  # 注册页面
    if request.method == 'POST':
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            username = user_create_form.cleaned_data.get('username')
            email = user_create_form.cleaned_data.get('email')
            password = user_create_form.cleaned_data.get('password1')

            user = User.objects.create_user(username=username, email=email, password=password)
            auth.login(request, user)
            return render(request, 'login/register_successfully.html')
        else:  # 未通过
            return render(request, 'login/register.html', {'user_create_form': user_create_form})
    else:  # 当正常访问时
        user_create_form = UserCreateForm
        return render(request, 'login/register.html', {'user_create_form': user_create_form})
