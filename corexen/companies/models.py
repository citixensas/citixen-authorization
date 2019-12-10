from uuid import uuid4

from django.db import models

from corexen.internationalization.models import City, Country, LanguageCode
from corexen.utils.models import CitixenModel, RandomFileName


class Company(CitixenModel):
    """Company model."""

    nit = models.CharField(max_length=50)
    name = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='companies')
    image_url = models.ImageField(upload_to=RandomFileName('companies/images/'))
    namespace = models.CharField(max_length=60, unique=True)

    is_active = models.BooleanField(default=False)

    uuid = models.UUIDField(default=uuid4, primary_key=True)

    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='companies')

    def __str__(self):
        return self.name


class Headquarter(CitixenModel):
    """Headquarter model."""

    uuid = models.UUIDField(default=uuid4, primary_key=True)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    description = models.TextField(null=True, blank=True)

    name = models.CharField(max_length=120, unique=True)
    image_url = models.ImageField(upload_to=RandomFileName('headquarters/images/'))

    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=120)
    neighborhood = models.CharField(max_length=120, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='headquarters')
    language_code = models.ForeignKey(LanguageCode, on_delete=models.PROTECT, related_name='headquarters')

    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='headquarters')

    def activate_or_deactivate(self):
        self.is_active = not self.is_active
        self.save()

    def mark_as_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'{self.name} is a headquarters of {self.company.name}'
