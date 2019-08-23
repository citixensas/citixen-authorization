from django.contrib import admin

from .models import User, UserPermission

admin.site.register(User)
admin.site.register(UserPermission)
