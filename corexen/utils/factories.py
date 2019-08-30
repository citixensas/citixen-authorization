import factory
from factory.django import DjangoModelFactory
from faker import Faker

from corexen.companies.models import Company, Headquarter

fake = Faker()


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    nit = fake.numerify()
    name = factory.Sequence(lambda n: f'company_{n}')
    email = fake.email()
    country = fake.country()
    image_url = fake.url()
​

class HeadquarterFactory(DjangoModelFactory):
    class Meta:
        model = Headquarter
​
    name = factory.Sequence(lambda n: f'headquarter_{n}')
    image_url = fake.url()
    address = fake.address()
    city = fake.city()
    country = fake.country()
