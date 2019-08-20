"""Companies factories."""

import uuid

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from companies.models import Company, Headquarter

fake = Faker()


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: 'company_%d' % n)
    created_by = uuid.uuid4()


class HeadquarterFactory(DjangoModelFactory):
    class Meta:
        model = Headquarter

    name = factory.Sequence(lambda n: 'headquarter_%d' % n)
    address = fake.address()
