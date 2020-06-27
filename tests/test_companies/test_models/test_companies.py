from django.db import IntegrityError
from faker import Faker
from test_plus import TestCase

from corexen.companies.models import Company, Headquarter
from corexen.internationalization.models import Country, City
from tests.test_companies.factories import HeadquarterFactory, CompanyFactory, CountryFactory, CityFactory

fake = Faker()


class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.country = Country.objects.create(name='Colombia')

    def test_return_company_string_representation(self):
        company = CompanyFactory(
            name='Compañía de prueba',
            country=self.country,
            created_by=self.user)
        self.assertEqual('Compañía de prueba', company.__str__())

    def test_should_not_create_company_with_the_same_name(self):
        Company.objects.create(
            name='test company',
            country=self.country,
            created_by=self.user)
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            **{'name': 'Test company', 'country': self.country, 'created_by': self.user}
        )

    def test_should_softdelete_CompanyFactory(self):
        company = CompanyFactory()
        uuid = company.pk

        company.delete()

        exists = Company.objects.filter(pk=uuid).exists()

        self.assertFalse(exists)

        exists = Company.original_objects.filter(pk=uuid).exists()

        self.assertTrue(exists)


class HeadquarterModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = self.make_user()
        self.country = CountryFactory(name='Colombia')
        self.city = CityFactory(
            country=self.country,
            google_map_key='key',
            code=5001,
            type=City.Types.locality
        )
        self.company = CompanyFactory(
            name='test company',
            country=self.country,
            created_by=self.user,
            namespace='testcompany')
        self.headquarter = HeadquarterFactory(
            company=self.company, name='test headquarter', address='address',
            city=self.city, created_by=self.user
        )

    def test_should_create_headquarters_with_the_same_name_in_different_companies_and_cities(self):
        other_city = CityFactory(
            name='city #2',
            country=self.country,
            google_map_key='key #2',
            code=5002,
            type=City.Types.locality
        )
        other_company = CompanyFactory(
            name='test company #2',
            country=self.country,
            created_by=self.user,
            namespace='testcompany2'
        )

        other_headquarter = HeadquarterFactory(
            **{
                'company': other_company,
                'name': 'test headquarter',
                'address': 'test #2 address',
                'city': other_city,
                'created_by': self.user
            }
        )

        self.assertIsNotNone(other_headquarter)

    def test_should_create_headquarters_with_the_same_name_in_the_same_city(self):
        # Even if the companies doesn't the same.
        other_company = CompanyFactory(
            name='test company #2',
            country=self.country,
            created_by=self.user,
            namespace='testcompany2'
        )

        other_headquarter = HeadquarterFactory(
            **{
                'company': other_company,
                'name': 'test headquarter',
                'address': 'test #2 address',
                'city': self.city,
                'created_by': self.user
            }
        )

        self.assertIsNotNone(other_headquarter)

    def test_should_create_headquarters_with_the_same_name_in_the_same_CompanyFactory(self):
        other_city = CityFactory(
            name='city #2',
            country=self.country,
            google_map_key='key #2',
            code=5002,
            type=City.Types.locality
        )

        other_headquarter = HeadquarterFactory(
            **{
                'company': self.company,
                'name': 'test headquarter',
                'address': 'test #2 address',
                'city': other_city,
                'created_by': self.user
            }
        )

        self.assertIsNotNone(other_headquarter)

    def test_should_softdelete_headquarter(self):
        headquarter = HeadquarterFactory()
        uuid = headquarter.pk

        headquarter.delete()

        exists = Headquarter.objects.filter(pk=uuid).exists()

        self.assertFalse(exists)

        exists = Headquarter.original_objects.filter(pk=uuid).exists()

        self.assertTrue(exists)
