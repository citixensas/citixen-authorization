from django.test import override_settings

from corexen.users.interactors import UserInteractor
from corexen.users.models import AppUser
from corexen.utils.testing import CitixenAPITestCase
from faker import Faker

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

    def test_create_user_success(self):
        UserInteractor.create_user(**self.valid_data)
        self.assertEquals(AppUser.objects.count(), 1)
        app_user = AppUser.objects.get()

    def test_create_user_fail_without_valid_data(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'username': '',
            'password': '',
            'password_confirmation': ''
        }
        created, app_user = UserInteractor.create_user(**data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    def test_create_user_fail_already_exist(self):
        UserInteractor.create_user(**self.valid_data)
        created, app_user = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)

    @override_settings(BASE_AUTHENTICATION_URL_API="http://127.0.0.1:8000/random_404/")
    def test_create_user_fail_404(self):
        created, app_user = UserInteractor.create_user(**self.valid_data)
        self.assertFalse(created)
        self.assertIsNone(app_user)
