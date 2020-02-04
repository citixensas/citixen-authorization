from django.db import models

from corexen.utils.models import CitixenModel, RandomFileName


class LatLngBounds(models.Model):
    name = models.CharField(max_length=120, null=True)
    northeast_latitude = models.DecimalField(max_digits=18, decimal_places=15, default=0)
    northeast_longitude = models.DecimalField(max_digits=18, decimal_places=15, default=0)
    southwest_latitude = models.DecimalField(max_digits=18, decimal_places=15, default=0)
    southwest_longitude = models.DecimalField(max_digits=18, decimal_places=15, default=0)

    def __str__(self):
        return f'{self.name}: NE[{self.northeast_latitude} - {self.northeast_longitude}] - ' \
               f'SW[{self.southwest_latitude} - {self.southwest_longitude}] '


class Country(CitixenModel):
    """Country model."""

    name = models.CharField(max_length=120, unique=True)
    national_flag = models.ImageField(upload_to=RandomFileName('country/images/'))

    calling_code = models.CharField(max_length=9, default='')

    class Meta:
        """Meta options."""
        ordering = ('name',)

    def __str__(self):
        return self.name


class City(CitixenModel):
    """City model."""

    name = models.CharField(max_length=120, unique=True)
    flag = models.ImageField(upload_to=RandomFileName('city/images/'))
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    google_map_key = models.CharField(max_length=150)
    map_bounds = models.OneToOneField(LatLngBounds, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        """Meta options."""
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} is a city of {self.country.name}'


class LanguageCode(CitixenModel):
    """LanguageCode model."""

    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=120, unique=True)

    class Meta:
        """Meta options."""
        ordering = ('code',)

    def __str__(self):
        return f'{self.code} - {self.name}'
