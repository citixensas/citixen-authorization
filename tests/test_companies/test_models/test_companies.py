from faker import Faker
from test_plus import TestCase

from corexen.companies.models import Company
from corexen.internationalization.models import Country

fake = Faker()


class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_return_company_string_representation(self):
        country = Country.objects.create(name='Colombia')
        company = Company.objects.create(
            name='Compañía de prueba',
            country=country,
            created_by=self.user)
        self.assertEqual('Compañía de prueba', company.__str__())

