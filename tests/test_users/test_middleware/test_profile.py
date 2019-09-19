import sys
from importlib import import_module

from django.core.exceptions import PermissionDenied, ImproperlyConfigured

from corexen.users.middleware import CitixenProfileMiddleware
from corexen.users.profiles import BaseProfileFinder
from corexen.utils.testing import CitixenAPITestCase
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import override_settings, RequestFactory
from django.urls import path, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class ProfileFinder(BaseProfileFinder):
    def get(self):
        if self.app and self.headquarter:
            profile = 'Object profile'
        else:
            profile = None
        return profile


class View(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request):
        return Response(data=request.user.profile, status=200)


urls = [
    path(r'^view/', View.as_view(), name='view'),
]
urlpatterns = import_module(settings.ROOT_URLCONF).urlpatterns + urls


@override_settings(
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        "corexen.users.middleware.JWTAuthenticationMiddleware",
        "tests.test_users.test_middleware.test_profile.CitixenProfileMiddleware",
    ]
)
class TestProfileMiddlewareTestCase(CitixenAPITestCase):
    def setUp(self) -> None:
        self.user = self.make_user()
        self.factory = RequestFactory()

    @override_settings(CITIXEN={})
    def test_assert_except_when_keywords_config_is_invalid(self):
        with self.login(self.user):
            with self.assertRaises(ImproperlyConfigured) as e:
                self.client.get(reverse('view'), format='json')
            self.assertEqual(str(e.exception), 'Some keywords for profile middleware were not provided')

    @override_settings(CITIXEN={
        'HEADQUARTER_IDENTIFIER': '',
        'APPLICATION_IDENTIFIER': '',
        'PROFILE_FINDER': ''
    })
    def test_assert_except_when_profile_finder_is_invalid(self):
        with self.login(self.user):
            with self.assertRaises(ImproperlyConfigured) as e:
                self.client.get(reverse('view'), format='json')
            self.assertEqual(str(e.exception), 'Profile finder for middleware not configured correctly')

    def test_without_process_view(self):
        with self.login(self.user):
            request = self.factory.get(reverse('view'), **self.extra_header(1, 2))
            SessionMiddleware().process_request(request)
            AuthenticationMiddleware().process_request(request)
            CitixenProfileMiddleware().process_request(request)
            self.assertEqual(request.user.profile, 'Object profile')

    def test_with_extra_headers(self):
        with self.login(self.user):
            url = reverse('view')
            response = self.get(url, extra=self.extra_header(1, 2))
            self.assertEqual(response.data, 'Object profile')

    def test_assert_except_when_profile_is_invalid(self):
        with self.login(self.user):
            response = self.get(reverse('view'), extra=self.extra_header(None, None))
            self.response_403(response)
