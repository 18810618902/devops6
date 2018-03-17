# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Django自带的内联模板格式
class ProfileInline(admin.StackedInline):     # 指定需要内联的model及展示样式
    model = UserProfile
    max_num = 1
    can_delete = False

class UserProfileAdmin(UserAdmin):     # 内联：当显示User数据的时候，也会显示UserProfile的数据
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

