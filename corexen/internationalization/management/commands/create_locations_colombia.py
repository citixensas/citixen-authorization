import json

from django.core.management.base import BaseCommand

from corexen.internationalization.management.utils import ManageInternationalization
from corexen.internationalization.models import Country


class Command(BaseCommand):
    help = 'Creation or Update Colombia'

    def handle(self, *args, **options):
        def print_msg(str_msg):
            self.stdout.write(self.style.SUCCESS(str_msg))

        # ###############SUPERUSER#########################
        print_msg('Start Creation Country')
        ManageInternationalization.create_country(
            name='Colombia',
            calling_code='57',
            administrative_area_level=Country.AdministrativeAreaLevel.administrative_area_level_2,
            administrative_area_level_1_name='DEPARTAMENTO',
            administrative_area_level_2_name='MUNICIPIO',
            administrative_area_level_3_name='CORREGIMIENTO',
        )

        # Load data Administrative Area Level 1
        with open('../data/colombia_administrative_area_level_1.json') as json_file:
            data = json.load(json_file)
            for p in data:
                print('administrative_area_level_1: ' + p['administrative_area_level_1'])

        # Load data Locality
        with open('../data/colombia.json') as json_file:
            data = json.load(json_file)
            for p in data:
                print('locality: ' + p['locality'])

        # endregion

        self.stdout.write(self.style.SUCCESS('Successfully Created Colombia'))
