from django.contrib import admin

from .models import Country, City, LanguageCode


admin.site.register(LanguageCode)


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
    list_display = ('id', 'name', 'parent', 'type', 'bounds')
    list_filter = ('type',)
    raw_id_fields = ('country', 'parent')
    search_fields = (
        'name',
        'code',
        'type',
        'google_map_key'
    )
    ordering = ('-id',)

    def get_queryset(self, request):
        return super(LocationAreaAdmin, self).get_queryset(request).select_related('parent', 'parent__country')
