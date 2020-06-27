"""Companies factories."""

import uuid
from decimal import Decimal

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from corexen.companies.models import Company, Headquarter
from corexen.internationalization.models import Country, City
from tests.test_users.factories import UserFactory

fake = Faker()


class CountryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f'country_{n}')

    class Meta:
        model = Country


class CityFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f'city_{n}')
    country = factory.SubFactory(CountryFactory)
    bounds = {
        'northeast': {'lat': 10.501783, 'lng': -73.222143},
        'southwest': {'lat': 10.427229, 'lng': -73.2943559}
    }
    google_map_key = factory.Sequence(lambda n: f'google_map_key{n}')

    class Meta:
        model = City


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    nit = fake.numerify()
    name = factory.Sequence(lambda n: f'company_{n}')
    namespace = factory.Sequence(lambda n: f'namespace_{n}')
    email = fake.email()
    country = factory.SubFactory(CountryFactory)
    is_active = True
    created_by = factory.SubFactory(UserFactory)


class HeadquarterFactory(DjangoModelFactory):
    class Meta:
        model = Headquarter

    name = factory.Sequence(lambda n: f'headquarter_{n}')
    address = fake.address()
    email = factory.Sequence(lambda n: f'user{n}_{fake.email()}')
    phone = factory.Sequence(lambda n: f'+57{n + 3128751348}')
    city = factory.SubFactory(CityFactory)
    company = factory.SubFactory(CompanyFactory)
    created_by = factory.SubFactory(UserFactory)
    latitude = fake.longitude().quantize(Decimal('.000000000000000'))
    longitude = fake.longitude().quantize(Decimal('.000000000000000'))
