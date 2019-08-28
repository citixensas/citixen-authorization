from django.conf.urls import url
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from corexen.utils.testing import CitixenAPITestCase
from tests.constants import EXAMPLE_TOKEN_VALID, EXAMPLE_TOKEN_INVALID


class PostView(APIView):
    def post(self, request):
        return Response(data=request.data, status=200)


class PostWithAuthView(PostView):
    permission_classes = (IsAuthenticated,)


urlpatterns = [
    url(r'^post$', PostView.as_view()),
    url(r'^post_login$', PostWithAuthView.as_view()),
]


class TestMiddlewareTestCase(CitixenAPITestCase):
    def test_can_access_request_post_without_login_required(self):
        response = self.client.post('/post', {'foo': 'bar'})
        self.response_200(response)
        response = self.client.post('/post', {'foo': 'bar'}, format='json')
        self.response_200(response)
        self.assertEquals(response.data, {'foo': 'bar'})

    def test_not_can_access_request_post_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % EXAMPLE_TOKEN_INVALID)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_401(response)

    def test_can_access_request_post_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % EXAMPLE_TOKEN_VALID)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_200(response)