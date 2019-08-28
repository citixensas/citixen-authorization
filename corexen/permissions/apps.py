"""Permissions apps"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsConfig(AppConfig):
    name = "corexen.permissions"
    verbose_name = _("Permission")

    def ready(self):
        try:
            from corexen.permissions.signals import *
        except ImportError:
            pass
