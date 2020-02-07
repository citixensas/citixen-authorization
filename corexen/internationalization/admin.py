from django.contrib import admin

from .models import Country, Location, LanguageCode, LatLngBounds

admin.site.register(Country)
admin.site.register(Location)
admin.site.register(LatLngBounds)
admin.site.register(LanguageCode)
