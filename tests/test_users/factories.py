import factory
from factory.django import DjangoModelFactory
from faker import Faker

from corexen.users.models import User

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name', locale='es_ES')
    last_name = factory.Faker('last_name', locale='es_ES')
    email = factory.Sequence(lambda n: f'user{n}_{fake.email()}')
    username = factory.Sequence(lambda n: f'{fake.user_name()}_{n}')
    password = factory.PostGenerationMethodCall('set_password', '*Mypassword12345.@#')
