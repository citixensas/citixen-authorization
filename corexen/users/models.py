from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4

from corexen.companies.models import Headquarter
from corexen.utils.models import CitixenModel


class User(CitixenModel, AbstractUser):
    uuid = models.UUIDField(default=uuid4, unique=True)
    user_permissions = models.ManyToManyField('auth.Permission', through='users.UserPermission')


class UserPermission(CitixenModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.DO_NOTHING)

    headquarter = models.ForeignKey(Headquarter, on_delete=models.DO_NOTHING)
