from faker import Faker
from test_plus import TestCase

from corexen.companies.models import Company

fake = Faker()


class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_return_company_string_representation(self):
        company = Company.objects.create(name='Compañía de prueba', created_by=self.user)
        self.assertEqual('Compañía de prueba', company.__str__())

