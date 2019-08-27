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
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "corexen.users.backends.AuthenticationBackend",
]

SITE_ID = 1

MIDDLEWARE = [
    "corexen.users.middleware.JWTAuthenticationMiddleware",
]
ADMIN_URL = "admin/"

# Django REST Framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'corexen.users.authentication.CitixenAuthentication',
    ),
}
