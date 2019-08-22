from django.contrib.auth import models as auth_models
from django.db import models
from django.contrib.auth.models import AbstractUser

from corexen.utils.models import CitixenModel


class User(CitixenModel, AbstractUser):
    # User permissions in headquarter.
    permissions = models.ManyToManyField(
        auth_models.Permission,
        through='users.UserPermission',
        related_name='permissions'
    )
