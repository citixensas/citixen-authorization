from django.db import models

from corexen.utils.models import CitixenModel, RandomFileName


class Country(CitixenModel):
    """Country model."""

    name = models.CharField(max_length=120, unique=True)
    national_flag = models.ImageField(upload_to=RandomFileName('country/images/'))

    def __str__(self):
        return self.name


class City(CitixenModel):
    """City model."""

    name = models.CharField(max_length=120, unique=True)
    image_url = models.ImageField(upload_to=RandomFileName('city/images/'))
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} is a city of {self.country.name}'


class LanguageCode(CitixenModel):
    """LanguageCode model."""

    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return f'{self.code} - {self.name}'
