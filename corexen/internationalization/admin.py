from django.contrib import admin

from .models import Country, City, LanguageCode, LatLngBounds

admin.site.register(Country)
admin.site.register(City)
admin.site.register(LatLngBounds)
admin.site.register(LanguageCode)
