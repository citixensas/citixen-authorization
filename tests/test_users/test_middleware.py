from django.conf.urls import url
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from corexen.utils.testing import CitixenAPITestCase


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
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi' \
                'wiZXhwIjoxNTYzODAzMDQ5LCJqdGkiOiI0NTU4M2FiY2JjZTY0N2MzOWUyNDgwYzg3Z' \
                'WRjNDc3MyIsInVzZXJfaWQiOjF9.VJXPtY3vh1-2EdPMORL_b9aMPpE7CQveg6akuWEwmmM'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % token)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_403(response)

    def test_can_access_request_post_with_valid_token(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiw' \
                'iZXhwIjoxNTY3NzgxNjAwLCJqdGkiOiIzNWE3OTQwMzE3Zjc0YmNjYWE4ZTM1N2EwY2R' \
                'jZGQ4NCIsInVzZXJfaWQiOjEwNSwiZmlyc3RfbmFtZSI6Ik5pY29sZSIsImxhc3RfbmF' \
                'tZSI6IldhbGxhY2UiLCJlbWFpbCI6ImpvaG4yNUBjYXJ0ZXIuY29tIiwidXNlcm5hbWUi' \
                'OiJsb2dhbjA0IiwidXVpZCI6IjBmMDYwMzA2LTdhYWItNDJlNy04MDJlLTkyM2JlZTVm' \
                'MWY5NCJ9.UrKMoEYes-4LDr2pVQl-RkcSiZ4Nfn0l22-qjn5rgZM'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % token)
        response = self.client.post('/post_login', {'foo': 'bar'}, format='json')
        self.response_200(response)
