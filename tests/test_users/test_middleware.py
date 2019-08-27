from django.conf.urls import url

from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.views import APIView

from corexen.utils.testing import CitixenAPITestCase


class PostView(APIView):
    def post(self, request):
        return Response(data=request.data, status=200)


urlpatterns = [
    url(r'^post$', PostView.as_view()),
]


class TestMiddleware(CitixenAPITestCase):

    def test_middleware_can_access_request_post_when_processing_response(self):
        response = self.client.post('/post', {'foo': 'bar'})
        self.response_200(response)
        response = self.client.post('/post', {'foo': 'bar'}, format='json')
        assert response.status_code == 200
        self.response_200(response)
        self.assertEquals(response.data, {'foo': 'bar'})
