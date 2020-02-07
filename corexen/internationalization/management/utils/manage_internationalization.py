from decimal import Decimal

from corexen.internationalization.models import Country, Location, LanguageCode, LatLngBounds
from corexen.utils.shortcuts import get_object_or_none


class ManageInternationalization:

    @staticmethod
    def create_country(
        name,
        administrative_area_level,
        calling_code,
        administrative_area_level_1_name='',
        administrative_area_level_2_name='',
        administrative_area_level_3_name='',
        national_flag='country/flag.jpg'
    ):
        country = get_object_or_none(Country, name=name)
        if not country:
            country = Country.objects.create(
                name=name,
                administrative_area_level=administrative_area_level,
                administrative_area_level_1_name=administrative_area_level_1_name,
                administrative_area_level_2_name=administrative_area_level_2_name,
                administrative_area_level_3_name=administrative_area_level_3_name,
                calling_code=calling_code,
                national_flag=national_flag)
        return country

    @staticmethod
    def create_location(name, country, google_map_key, map_bounds=None, flag='location/flag.jpg'):
        location = get_object_or_none(Location, name=name)
        if not location:
            if not map_bounds:
                map_bounds = LatLngBounds.objects.create(
                    name=name,
                    northeast_latitude=Decimal("10.503767000000000"),
                    northeast_longitude=Decimal("-73.224466000000000"),
                    southwest_latitude=Decimal("10.425625000000000"),
                    southwest_longitude=Decimal("-73.301382000000000")
                )
            location = Location.objects.create(
                name=name,
                country=country,
                google_map_key=google_map_key,
                map_bounds=map_bounds,
                flag=flag
            )
        return location

    @staticmethod
    def create_language_code(name, code):
        language_code = get_object_or_none(LanguageCode, code=code)
        if not language_code:
            language_code = LanguageCode.objects.create(name=name, code=code)
        return language_code
