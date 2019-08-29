from faker import Faker
from test_plus import TestCase

from corexen.companies.models import Company
from corexen.users.models import AppUser

fake = Faker()


class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.appUser = AppUser.objects.create()

    def test_return_company_string_representation(self):
        company = Company.objects.create(name='Compañía de prueba', created_by=self.appUser)
        self.assertEqual('Compañía de prueba', company.__str__())

