from django.contrib import admin

from .models import Country, City, LanguageCode, LatLngBounds


admin.site.register(LanguageCode)


@admin.register(LatLngBounds)
class LatLngBoundsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'northeast_latitude', 'northeast_longitude', 'southwest_latitude', 'southwest_longitude')
    search_fields = (
        'name',
    )
    ordering = ('-id',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'administrative_area_level', 'calling_code')
    list_filter = ('administrative_area_level',)
    search_fields = (
        'name',
        'administrative_area_level',
        'calling_code'
    )
    ordering = ('-id',)


@admin.register(City)
class LocationAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'country', 'type', 'map_bounds')
    list_filter = ('country', 'type')
    search_fields = (
        'name',
        'code',
        'type',
        'google_map_key'
    )
    ordering = ('-id',)
