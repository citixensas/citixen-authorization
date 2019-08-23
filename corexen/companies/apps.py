from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompaniesConfig(AppConfig):
    name = "companies"
    verbose_name = _("Companies")

    def ready(self):
        try:
            from corexen import companies
        except ImportError:
            pass
