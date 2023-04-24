from django.urls import re_path
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from corexen.utils.testing import CitixenAPITestCase
from tests.constants import EXAMPLE_TOKEN_INVALID


class PostView(APIView):
    def post(self, request):
        return Response(data=request.data, status=200)


class PostWithAuthView(PostView):
    permission_classes = (IsAuthenticated,)


class PostWithAppUser(PostWithAuthView):
    def post(self, request):
        return Response(data=request.user.pk, status=200)


urlpatterns = [
    re_path(r'^post$', PostView.as_view()),
    re_path(r'^post_login$', PostWithAuthView.as_view()),
    re_path(r'^post_app_user$', PostWithAppUser.as_view()),
]


class TestMiddlewareTestCase(CitixenAPITestCase):
    def setUp(self) -> None:
        self.user = self.make_user()

    def test_can_access_request_post_without_login_required(self):
        response = self.client.post('/post', {'foo': 'bar'})
        self.response_200(response)
        response = self.client.post('/post', {'foo': 'bar'}, format='json')
        self.response_200(response)
        self.assertEqual(response.data, {'foo': 'bar'})

    def test_not_can_access_request_post_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % EXAMPLE_TOKEN_INVALID)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_403(response)

    def test_can_access_request_post_with_valid_token(self):
        self.set_client_token(self.user)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_200(response)

    def test_can_access_app_user_from_request(self):
        self.set_client_token(self.user)
        response = self.client.post('/post_app_user', {'foo': 'bar'}, format='json')
        self.response_200(response)
        self.assertEqual(response.data, self.user.pk)
