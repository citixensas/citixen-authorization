# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import environ
from django.utils.translation import ugettext_lazy as _

env = environ.Env()

SECRET_KEY = "Jb4KwtjG4CTOc3ZviJGrxSsNecosF9n5ODbUker3rmd4GdZF4i7Zd79hDbonb0RD"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_DIR = (
    environ.Path(__file__) - 3
)
APPS_DIR = ROOT_DIR.path("corexen")

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "America/Bogota"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "es-co"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

LANGUAGES = (
   ('en', _('English')),
   ('es-co', _('Spanish colombia')),
)

ROOT_URLCONF = "tests.urls"

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

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    "corexen.users.middleware.JWTAuthenticationMiddleware",
]
ADMIN_URL = "admin/"

# Django REST Framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
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
