# coding: utf-8
# 定义模型，包括：用户模型以及用户管理器

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, validators=[validate_phone])
    email = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user.id)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

        def get_short_name(self):
            return str(self.username)

        def has_perm(self, perm, obj=None):
            return True

        def has_module_perms(self, app_label):
            return True

        @property
        def is_staff(self):
            return self.is_admin

