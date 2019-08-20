from django.contrib import admin

from .models import Headquarter
from companies.models import Company

admin.site.register(Company)
admin.site.register(Headquarter)
