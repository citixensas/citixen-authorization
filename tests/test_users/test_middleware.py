from django.conf.urls import url
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.views import APIView

from corexen.utils.testing import CitixenAPITestCase


class PostView(APIView):
    def post(self, request):
        return Response(data=request.data, status=200)


class PostWithAuthView(LoginRequiredMixin, PostView):
    pass


urlpatterns = [
    url(r'^post$', PostView.as_view()),
    url(r'^post_login$', PostWithAuthView.as_view()),
]


class TestMiddleware(CitixenAPITestCase):

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
        assert response.status_code == 302
