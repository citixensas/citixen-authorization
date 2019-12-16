"""Citixen test utilities."""

from django.contrib.auth.models import Permission
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from test_plus import APITestCase, TestCase

from corexen.users.models import UserPermission
from configs.settings import test

fake = Faker()


class CitixenTestCase(TestCase):
    """Base citixen test case."""

    user = None
    headquarter = None

    def _add_user_permission(self, perm, user, headquarter):
        """Add single user permission only if permission exists on db."""
        permission = Permission.objects.filter(codename=perm).first()
        if permission:
            UserPermission.objects.create(user=user, permission=permission,
                                          headquarter=headquarter)

    def _add_user_permissions(self, perms, user=None, headquarter=None):
        """Add permissions to user from perm codename list."""
        user = user or self.user
        headquarter = headquarter or self.headquarter
        for perm in perms:
            self._add_user_permission(perm, user, headquarter)

    def make_superuser(self, **kwargs):
        user = self.make_user(**kwargs)
        user.is_superuser = True
        user.save()
        return user

    def generate_factory_profile(self, profile, **kwargs):
        """
        Generic profile factory generator
        :param profile: Profile factory
        :param kwargs: Factory params
        :return: Two values, first the profile and second the AppUser
        """
        user = self.make_user(username=fake.user_name())
        profile = profile(uuid=user.uuid, **kwargs)
        return profile, user


class Login(object):

    def __init__(self, test_case, user):
        self.user = user
        self.test_case = test_case

    def __enter__(self):
        self.test_case.set_client_token(user=self.user)

    def __exit__(self, *args):
        self.test_case.remove_client_token(user=self.user)


class CitixenAPITestCase(CitixenTestCase,
                         APITestCase):
    """Citixen api test case."""

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return tokens

    def set_client_token(self, user):
        self._access_token = self.get_tokens_for_user(user).get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self._access_token)

    def remove_client_token(self, user):
        self.client.credentials(HTTP_AUTHORIZATION='')

    def login(self, user):
        """ Login a user """
        return Login(self, user)

    @staticmethod
    def extra_header(app, headquarter):
        return {
            test.CITIXEN['APPLICATION_IDENTIFIER']: app,
            test.CITIXEN['HEADQUARTER_IDENTIFIER']: headquarter,
        }
