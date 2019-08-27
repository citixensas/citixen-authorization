# -*- coding: utf-8 -*-
from django.urls import include
from tests.test_users.test_middleware import urlpatterns as middleware_url

urlpatterns = []

urlpatterns += middleware_url
