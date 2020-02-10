from corexen.internationalization.models import Country, LocationArea, LanguageCode, LatLngBounds
from corexen.utils.shortcuts import get_object_or_none


class ManageInternationalization:

    @staticmethod
    def get_or_create_country(instance_country):
        country = get_object_or_none(Country, name=instance_country.name)
        if not country:
            instance_country.save()
            return instance_country
        return country

    @staticmethod
    def get_or_create_location(instance_location: LocationArea, instance_bounds: LatLngBounds):
        location = get_object_or_none(LocationArea, code=instance_location.code, country=instance_location.country.pk)
        if not location:
            instance_bounds.save()
            instance_location.map_bounds_id = instance_bounds.pk
            instance_location.save()
            return instance_location
        return location

    @staticmethod
    def create_language_code(name, code):
        language_code = get_object_or_none(LanguageCode, code=code)
        if not language_code:
            language_code = LanguageCode.objects.create(name=name, code=code)
        return language_code
