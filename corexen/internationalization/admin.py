import json
import logging

from django.contrib import admin
from django.forms import widgets

from .models import Country, City, LanguageCode
from ..utils.models import JSONField

logger = logging.getLogger(__name__)

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


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


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
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def get_queryset(self, request):
        return super(LocationAreaAdmin, self).get_queryset(request).select_related('parent', 'parent__country')
