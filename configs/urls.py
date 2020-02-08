# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import path
from django.contrib import admin
from tests.test_users.test_middleware.test_authentication import urlpatterns as middleware_url

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
]

urlpatterns += middleware_url
