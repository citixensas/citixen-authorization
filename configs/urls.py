# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from tests.test_users.test_middleware.test_authentication import urlpatterns as middleware_url

urlpatterns = []

if not settings.TESTING:
    urlpatterns += [
        # Django Admin, use {% url 'admin:index' %}
        path(settings.ADMIN_URL, admin.site.urls),
    ]
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns += middleware_url
