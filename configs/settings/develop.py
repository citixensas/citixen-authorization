# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

import environ
from django.utils.translation import ugettext_lazy as _

ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (configs/settings/base.py - 3 = /)

APPS_DIR = ROOT_DIR.path('corexen')
DATA_DIR = ROOT_DIR.path('data')

env = environ.Env()

SECRET_KEY = "Jb4KwtjG4CTOc3ZviJGrxSsNecosF9n5ODbUker3rmd4GdZF4i7Zd79hDbonb0RD"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DATA_DIR, 'db.sqlite3'),
    }
}

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

ROOT_URLCONF = "configs.urls"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "corexen.companies",
    "corexen.internationalization",
    "corexen.users",
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "corexen.users.backends.AuthenticationBackend",
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corexen.users.middleware.JWTAuthenticationMiddleware",
]

STATIC_URL = '/static/'

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
