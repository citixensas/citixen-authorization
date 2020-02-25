import json
import os
import environ
from django.core.management.base import BaseCommand
from django.db import transaction

from corexen.internationalization.management.utils import ManageInternationalization
from corexen.internationalization.models import Country, City


class Command(BaseCommand):
    help = 'Creation or Update Colombia'
    ROOT_DIR = (
        environ.Path(__file__) - 5
    )
    DATA_DIR = ROOT_DIR.path('data')

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
                return google_data['geometry']['viewport']

            # Load data Administrative Area Level 1
            with open(os.path.join(self.DATA_DIR, 'colombia_administrative_area_level_1.json')) as json_file:
                data = json.load(json_file)
                for location in data:
                    print('administrative_area_level_1: ' + location['administrative_area_level_1'])
                    instance_location = City(
                        code=int(location['code_administrative_area_level_1']),
                        name=location['administrative_area_level_1'],
                        flag='locations/flag.jpg',
                        country=country,
                        parent=None,
                        type=City.Types.administrative_area_level_1,
                        bounds=generate_instance_bound(location['google']),
                        google_map_key=location['google']['formatted_address'],
                        geo_code_json=location['google']
                    )
                    instance_db = ManageInternationalization.get_or_create_location(
                        instance_location=instance_location
                    )
                    instances_administrative_area_level_1.update({
                        str(instance_location.code): instance_db
                    })

            instances_locality = {}
            # Load data Locality
            locality = 0
            with open(os.path.join(self.DATA_DIR, 'colombia.json')) as json_file:
                data = json.load(json_file)
                for location in data:
                    locality += 1
                    print('locality: ' + str(locality) + ' ' + location['locality'])

                    instance_location = City(
                        code=int(location['code_locality']),
                        name=location['locality'],
                        flag='locations/flag.jpg',
                        country=country,
                        parent=instances_administrative_area_level_1[str(location['code_administrative_area_level_1'])],
                        type=City.Types.locality,
                        bounds=generate_instance_bound(location['google']),
                        google_map_key=location['google']['formatted_address'],
                        geo_code_json=location['google']
                    )
                    instance_db = ManageInternationalization.get_or_create_location(
                        instance_location=instance_location
                    )
                    instances_locality.update({
                        str(instance_location.code): instance_db
                    })

            # endregion

            self.stdout.write(self.style.SUCCESS('Successfully Created Colombia'))
