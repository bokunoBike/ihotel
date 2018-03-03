# -*- coding: utf-8 -*-
# 定义除了用户创建表单和用户修改表单之外的其他表单,包括：登录表单

from django import forms


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(
        label='用户名',
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        # Check the format of username
        username = self.cleaned_data.get("username")
        if len(username) < 6 or len(username) > 14:
            raise forms.ValidationError("#用户名的长度应该在6到14个字符之间")
        return username

    def clean_password1(self):
        # Check the format of password
        password = self.cleaned_data.get("password1")
        if len(password) < 6 or len(password) > 12:
            raise forms.ValidationError("#密码的长度应该在6到12个字符之间")
        return password
