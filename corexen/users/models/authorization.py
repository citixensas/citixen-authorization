# """Users authorization models."""

from corexen.companies.models import Headquarter
from django.contrib.auth.models import Permission
from django.db import models

from django.contrib.auth import get_user_model
from corexen.utils.models import CitixenModel


class UserPermission(CitixenModel):
    """User permission model.

    Hold the user permission in companies and headquarters.
    - Headquarter permission: users.add_operator.1hq - Add operators in headquarter #1
    - Company permissoin:     users.add_operator.1c  - Add operators in company #1
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    headquarter = models.ForeignKey(
        Headquarter,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        """Return friendly description."""
        return '{user} can {perm} in {headquarter}'.format(
            user=self.user.username, perm=self.permission, headquarter=self.headquarter)
