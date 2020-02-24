from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class CreateLocationColombiaTest(TestCase):
    def test_should_command_create_colombia_output(self):
        out = StringIO()
        call_command('create_locations_colombia', stdout=out)
        self.assertIn('Successfully Created Colombia', out.getvalue())
