# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import Profile

# de-register from admin.auth
admin.site.unregister(User)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', ]


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)