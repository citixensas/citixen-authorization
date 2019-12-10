from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InternationalizationConfig(AppConfig):
    name = "corexen.internationalization"
    verbose_name = _("Internationalization")

    def ready(self):
        try:
            from corexen.internationalization.signals import *
        except ImportError:
            pass
