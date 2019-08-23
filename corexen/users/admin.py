from django.contrib import admin

from .models import UserPermission, User

admin.site.register(UserPermission)
admin.site.register(User)
