# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from datetime import timedelta

import django

DEBUG = True
USE_TZ = True

SECRET_KEY = "Jb4KwtjG4CTOc3ZviJGrxSsNecosF9n5ODbUker3rmd4GdZF4i7Zd79hDbonb0RD"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "corexen.companies",
    "corexen.users",
    "corexen.permissions",
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "corexen.users.backends.AuthenticationBackend",
]

SITE_ID = 1

MIDDLEWARE = [
    "corexen.users.middleware.JWTAuthenticationMiddleware",
    #   "tests.test_users.test_middleware.test_profile.CitixenProfileMiddleware",
]
ADMIN_URL = "admin/"

# Django REST Framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}


# JWT
# ------------------------------------------------------------------------------

SIMPLE_JWT = {
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'user_id',
}

# Corexen
# ------------------------------------------------------------------------------

BASE_AUTHENTICATION_URL_API = 'http://127.0.0.1:8000/api/'
URL_SIGNUP = 'authentication/signup/'
URL_USER_INFO = 'authentication/users/'

__header_format = lambda x: f'HTTP_{x}'.upper().replace('-', '_')
CITIXEN = {
    'HEADQUARTER_IDENTIFIER': __header_format('Headquarter-id'),
    'APPLICATION_IDENTIFIER': __header_format('App-id'),
    'PROFILE_FINDER': 'tests.test_users.test_middleware.test_profile.ProfileFinder'
}
