# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from .base import *

APPS_DIR = ROOT_DIR.path('corexen')
DATA_DIR = ROOT_DIR.path('data')

DEBUG = True

SECRET_KEY = "Jb4KwtjG4CTOc3ZviJGrxSsNecosF9n5ODbUker3rmd4GdZF4i7Zd79hDbonb0RD"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

TESTING = True

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "corexen.companies",
    "corexen.internationalization",
    "corexen.users",
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "corexen.users.backends.AuthenticationBackend",
]

SITE_ID = 1

MIDDLEWARE = [
    "corexen.users.middleware.JWTAuthenticationMiddleware",
]
