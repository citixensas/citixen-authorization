"""Permissions apps"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsConfig(AppConfig):
    name = "corexen.permissions"
    verbose_name = _("Permission")

    def ready(self):
        try:
            import corexen.permissions.signals  # pylint: disable=W0611
        except ImportError:
            pass
