# -*- coding: utf-8 -*-
from django.urls import include, path
from tests.test_users.test_middleware.test_authentication import urlpatterns as middleware_url
from corexen.permissions.urls import urlpatterns as permission_url

urlpatterns = [
    path('permissions/', include(('corexen.permissions.urls', 'corexen.permissions'), namespace='permissions'))
]

urlpatterns += middleware_url
