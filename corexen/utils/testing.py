"""Citixen test utilities."""

from django.contrib.auth.models import Permission
from rest_framework_simplejwt.tokens import RefreshToken
from test_plus import APITestCase, TestCase

from corexen.users.models import UserPermission, AppUser


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
        headquarter = self.headquarter or headquarter
        for perm in perms:
            self._add_user_permission(perm, user, headquarter)

    def make_superuser(self, **kwargs):
        user = self.make_user(**kwargs)
        user.is_superuser = True
        user.save()
        return user

    def make_remote_user(self, **kwargs):
        user = super().make_user(**kwargs)
        app_user = AppUser.objects.create(uuid=user.uuid)
        return user, app_user


class CitixenAPITestCase(CitixenTestCase,
                         APITestCase):
    """Citixen api test case."""

    @staticmethod
    def get_tokens_for_user(user):
        token = RefreshToken.for_user(user)
        token.payload.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'uuid': str(user.uuid)
        })
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

    def set_client_token(self, user):
        self._access_token = self.get_tokens_for_user(user).get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self._access_token)
