from django.contrib import admin

from .models import Headquarter
from corexen.companies import Company

admin.site.register(Company)
admin.site.register(Headquarter)
