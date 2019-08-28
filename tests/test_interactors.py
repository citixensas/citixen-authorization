import uuid

import requests_mock
from django.test import override_settings
from faker import Faker

from corexen.users.interactors import UserInteractor
from corexen.users.models import AppUser
from corexen.utils.testing import CitixenAPITestCase

fake = Faker()


class UserInteractorTest(CitixenAPITestCase):
    def setUp(self):
        fake_name = fake.name()
        fake_password = fake.password()
        self.valid_data = {
            'first_name': fake_name.split()[0],
            'last_name': fake_name.split()[1],
            'email': fake.email(),
            'username': fake.user_name(),
            'password': fake_password,
            'password_confirmation': fake_password
        }

    @requests_mock.Mocker()
    def test_create_user_success(self, m):
        fake_uuid = str(uuid.uuid1())
        m.register_uri('POST', 'http://127.0.0.1:8000/api/authentication/signup/',
                       json={'uuid': fake_uuid}, status_code=201)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertTrue(created)
        self.assertEquals(AppUser.objects.count(), 1)
        self.assertEquals(app_user.uuid, fake_uuid)

    @requests_mock.Mocker()
    def test_create_user_fail_without_valid_data(self, m):
        m.register_uri('POST', 'http://127.0.0.1:8000/api/authentication/signup/', json={}, status_code=400)
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'username': '',
            'password': '',
            'password_confirmation': ''
        }
        created, app_user, remote_response = UserInteractor.create_user(**data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    @requests_mock.Mocker()
    def test_create_user_fail_already_exist(self, m):
        m.register_uri('POST', 'http://127.0.0.1:8000/api/authentication/signup/',
                       json={
                           'username': ['El nombre de usuario ya está en uso.'],
                           'email': ['El correo ya está en uso.']
                       },
                       status_code=400)
        UserInteractor.create_user(**self.valid_data)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)
        self.assertEquals(remote_response, {
            'username': ['El nombre de usuario ya está en uso.'],
            'email': ['El correo ya está en uso.']
        })

    @requests_mock.Mocker()
    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:8000/random_404/")
    def test_create_user_fail_404(self, m):
        m.register_uri('POST', 'http://127.0.0.1:8000/random_404/authentication/signup/', json={}, status_code=404)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:5732/api/")
    def test_create_user_fail_url_api_invalid(self):
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)
