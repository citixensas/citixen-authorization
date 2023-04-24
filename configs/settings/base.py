import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (configs/settings/base.py - 3 = /)

ROOT_URLCONF = "configs.urls"

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

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
