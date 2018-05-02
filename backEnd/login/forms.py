# -*- coding: utf-8 -*-
# 定义除了用户创建表单和用户修改表单之外的其他表单,包括：登录表单

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# 新增用户表单
class UserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(
        label='用户名',
    )
    email = forms.EmailField(
        label="邮箱"
    )
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("#密码不一致")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# 修改用户表单
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = ('username',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

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
