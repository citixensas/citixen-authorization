import json
import os
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from corexen.internationalization.management.utils import ManageInternationalization
from corexen.internationalization.models import Country, LocationArea, LatLngBounds


class Command(BaseCommand):
    help = 'Creation or Update Colombia'

    def handle(self, *args, **options):
        with transaction.atomic():
            def print_msg(str_msg):
                self.stdout.write(self.style.SUCCESS(str_msg))

            # ###############SUPERUSER#########################
            print_msg('Start Creation Country')
            country = Country(
                name='Colombia',
                calling_code='57',
                administrative_area_level=Country.AdministrativeAreaLevel.administrative_area_level_2,
                administrative_area_level_1_name='DEPARTAMENTO',
                administrative_area_level_2_name='MUNICIPIO',
                administrative_area_level_3_name='CORREGIMIENTO',
                national_flag='country/flag.jpg'
            )
            country = ManageInternationalization.get_or_create_country(country)

            instances_administrative_area_level_1 = {}

            def generate_instance_bound(google_data):
                return LatLngBounds(
                    name=google_data['formatted_address'],
                    northeast_latitude=Decimal(google_data['geometry']['viewport']['northeast']['lat']),
                    northeast_longitude=Decimal(google_data['geometry']['viewport']['northeast']['lng']),
                    southwest_latitude=Decimal(google_data['geometry']['viewport']['southwest']['lat']),
                    southwest_longitude=Decimal(google_data['geometry']['viewport']['southwest']['lng']),
                )

            # Load data Administrative Area Level 1
            with open(os.path.join(settings.DATA_DIR, 'colombia_administrative_area_level_1.json')) as json_file:
                data = json.load(json_file)
                for location in data:
                    print('administrative_area_level_1: ' + location['administrative_area_level_1'])
                    instance_location = LocationArea(
                        name=location['administrative_area_level_1'],
                        flag='locations/flag.jpg',
                        country=country,
                        parent=None,
                        code=int(location['code_administrative_area_level_1']),
                        type=LocationArea.Types.administrative_area_level_1,
                        google_map_key=location['google']['formatted_address'],
                        geo_code_json=location['google']
                    )
                    instance_bounds = generate_instance_bound(location['google'])
                    instance_db = ManageInternationalization.get_or_create_location(
                        instance_location=instance_location,
                        instance_bounds=instance_bounds
                    )
                    instances_administrative_area_level_1.update({
                        str(instance_location.code): instance_db
                    })

            instances_locality = {}
            # Load data Locality
            locality = 0
            with open(os.path.join(settings.DATA_DIR, 'colombia.json')) as json_file:
                data = json.load(json_file)
                for location in data:
                    locality += 1
                    print('locality: ' + str(locality) + ' ' + location['locality'])

                    instance_location = LocationArea(
                        name=location['locality'],
                        flag='locations/flag.jpg',
                        country=country,
                        parent=instances_administrative_area_level_1[str(location['code_administrative_area_level_1'])],
                        code=int(location['code_locality']),
                        type=LocationArea.Types.locality,
                        google_map_key=location['google']['formatted_address'],
                        geo_code_json=location['google']
                    )
                    instance_bounds = generate_instance_bound(location['google'])
                    instance_db = ManageInternationalization.get_or_create_location(
                        instance_location=instance_location,
                        instance_bounds=instance_bounds
                    )
                    instances_locality.update({
                        str(instance_location.code): instance_db
                    })

            # endregion

            self.stdout.write(self.style.SUCCESS('Successfully Created Colombia'))
