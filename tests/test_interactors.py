import uuid

import requests_mock
from django.test import override_settings
from faker import Faker
from requests.exceptions import ConnectTimeout, ConnectionError

from corexen.users.interactors import UserInteractor
from corexen.users.models import User
from corexen.utils.testing import CitixenAPITestCase

fake = Faker()


@requests_mock.Mocker(real_http=True)
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

    def test_create_user_success(self, m):
        fake_uuid = str(uuid.uuid1())
        m.register_uri('POST', 'http://127.0.0.1:8000/api/authentication/signup/',
                       json={'uuid': fake_uuid}, status_code=201)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertTrue(created)

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

    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:8000/random_404/")
    def test_create_user_fail_404(self, m):
        m.register_uri('POST', 'http://127.0.0.1:8000/random_404/authentication/signup/', json={}, status_code=404)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:5732/api/")
    def test_create_user_fail_connection_error(self, m):
        m.register_uri('POST', 'http://127.0.0.1:5732/api/authentication/signup/', exc=ConnectionError)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:5732/api/")
    def test_create_user_fail_connection_time_out(self, m):
        m.register_uri('POST', 'http://127.0.0.1:5732/api/authentication/signup/', exc=ConnectTimeout)
        created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    def test_retrive_user_info(self, m):
        user= self.make_user(username=self.valid_data['username'])
        user_id = str(user.uuid)
        m.register_uri('GET', f'http://127.0.0.1:8000/api/authentication/users/{user_id}',
                       json={
                           'username': user.username,
                           'email': user.email,
                           'uuid': user_id
                       }, status_code=200)
        #   created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        found, remote_response = UserInteractor.retrive_user_info(user=user)
        self.assertEquals(remote_response['username'], self.valid_data['username'])

    @override_settings(URL_USER_INFO="authentication/users_list/")
    def test_retrive_user_info_fail_when_server_handle_404(self, m):
        user = self.make_user(username=self.valid_data['username'])
        user_id = str(user.uuid)
        m.register_uri('POST', f'http://127.0.0.1:8000/random_404/authentication/users/{user_id}',
                       json={}, status_code=404)
        #   created, app_user, remote_response = UserInteractor.create_user(**self.valid_data)
        found, remote_response = UserInteractor.retrive_user_info(user=user)
        self.assertFalse(found)
        self.assertEquals(len(remote_response), 0)

    def test_convert_queryset_to_list(self, m):
        user1 = self.make_user(username='user1')
        user2 = self.make_user(username='user2')
        uuid_list = UserInteractor.convert_user_queryset_to_list_uuid(User.objects.all())
        self.assertEquals(len(uuid_list), 2)
        self.assertIn(str(user1.uuid), uuid_list)
        self.assertIn(str(user2.uuid), uuid_list)

    def test_convert_empty_queryset_to_list(self, m):
        uuid_list = UserInteractor.convert_user_queryset_to_list_uuid(User.objects.all())
        self.assertEquals(len(uuid_list), 0)

    def test_retrive_users_list(self, m):
        user = self.make_user(username=self.valid_data['username'])
        m.register_uri('POST', f'http://127.0.0.1:8000/api/authentication/users/',
                       json=[
                           {'uuid': str(user.uuid)}
                       ], status_code=200)
        response = UserInteractor.retrive_users_list(queryset=User.objects.all())
        self.assertEquals(len(response), 1)
        self.assertEquals(response[0]['uuid'], str(user.uuid))

    def test_retrive_users_empty_list(self, m):
        m.register_uri('POST', f'http://127.0.0.1:8000/api/authentication/users/', json=[], status_code=200)
        response = UserInteractor.retrive_users_list(queryset=User.objects.none())
        self.assertEquals(len(response), 0)


