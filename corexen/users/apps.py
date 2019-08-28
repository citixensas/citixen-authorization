from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "corexen.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import corexen.users.signals  # pylint: disable=W0611
        except ImportError:
            pass
