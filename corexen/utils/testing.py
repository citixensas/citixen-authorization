"""Citixen test utilities."""

from django.contrib.auth.models import Permission
from rest_framework_simplejwt.tokens import RefreshToken

from test_plus import APITestCase

#UserPermissionfrom citixen.users.models import


class CitixenAPITestCase(APITestCase):
    """Citixen api test case.

    This class add custom helper methods.
    """

    user = None
    headquarter = None

    def _add_user_permissions(self, perms, user=None, headquarter=None):
        """Add permissions to user from perm codename lst."""
        user = user or self.user
        headquarter = self.headquarter or headquarter
        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            #UserPermission.objects.create(user=user, permission=permission,
            #                              headquarter=headquarter)

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def set_client_token(self, user):
        self._access_token = self.get_tokens_for_user(user).get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self._access_token)

    def make_superuser(self, **kwargs):
        user = self.make_user(**kwargs)
        user.is_superuser = True
        user.save()
        return user
