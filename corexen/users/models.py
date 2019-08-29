from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from corexen.companies.models import Headquarter
from corexen.utils.models import CitixenModel


class RemoteUserModelMixin(CitixenModel):
    """This mixin expose unique idenfier."""

    uuid = models.UUIDField(default=uuid4, unique=True)

    class Meta:
        abstract = True


class AppUser(RemoteUserModelMixin):
    """This model will be used in each app that implements the authorization package."""

    def __str__(self):
        return 'Remote User: {uuid}'.format(uuid=self.uuid)


class User(RemoteUserModelMixin,
           AbstractUser):
    """This model contains user data in auth app and each citixen project."""

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        through='users.UserPermission')

    objects = UserManager()


class UserPermission(CitixenModel):
    """This model contains each permission for user in specific headquarter."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.DO_NOTHING)

    headquarter = models.ForeignKey(Headquarter, on_delete=models.DO_NOTHING)

    def __str__(self):
        """Return friendly description."""
        return '{user} can {perm} in {headquarter}'.format(
            user=self.user.username, perm=self.permission, headquarter=self.headquarter)
