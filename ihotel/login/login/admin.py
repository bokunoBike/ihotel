# coding: utf-8
# 注册自定义的用户，包括：新增用户表单、修改用户表单

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from login.models import User


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


# 注册用户
class MyUserAdmin(UserAdmin):
    form = UserCreateForm
    add_form = UserCreateForm

    list_display = ('username', 'created_at', 'email', 'is_delete', 'is_admin')
    search_fields = ('username', 'email')
    list_filter = ('is_admin',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'avatar',)}),
        ('Personal info', {'fields': ('created_at', 'updated_at')}),
        (
            'Open token info',
            {
                'fields': ('access_token', 'refresh_token', 'expires_in')
            }
        ),
        ('Permissions', {'fields': ('is_delete', 'is_admin', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            }
        ),
    )
    ordering = ('created_at',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)
