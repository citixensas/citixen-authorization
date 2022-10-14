from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _

from corexen.internationalization.constants import schema_location_area_bound
from corexen.utils.models import JSONField, CitixenModel, RandomFileName
from corexen.utils.validators import JSONSchemaValidator


class Country(CitixenModel):
    """Country model."""

    class AdministrativeAreaLevel(models.IntegerChoices):
        administrative_area_level_1 = 1
        administrative_area_level_2 = 2
        administrative_area_level_3 = 3
        administrative_area_level_4 = 4
        administrative_area_level_5 = 5

    name = models.CharField(max_length=120, unique=True)
    national_flag = models.ImageField(upload_to=RandomFileName('country/images/'))
    administrative_area_level = models.IntegerField(choices=AdministrativeAreaLevel.choices,
                                                    default=AdministrativeAreaLevel.administrative_area_level_2)
    administrative_area_level_1_name = models.CharField(max_length=90, null=True, blank=True)
    administrative_area_level_2_name = models.CharField(max_length=90, null=True, blank=True)
    administrative_area_level_3_name = models.CharField(max_length=90, null=True, blank=True)
    administrative_area_level_4_name = models.CharField(max_length=90, null=True, blank=True)
    administrative_area_level_5_name = models.CharField(max_length=90, null=True, blank=True)
    calling_code = models.CharField(max_length=9, default='')
    iso_code = models.CharField(max_length=6, default=None)

    class Meta:
        """Meta options."""
        ordering = ('name',)

    def __str__(self):
        return self.name


class City(CitixenModel):
    """location model."""

    class Types(models.TextChoices):
        locality = 'locality', _('Locality')
        administrative_area_level_1 = 'administrative_area_level_1', _('Administrative Area Level 1')
        administrative_area_level_2 = 'administrative_area_level_2', _('Administrative Area Level 2')
        administrative_area_level_3 = 'administrative_area_level_3', _('Administrative Area Level 3')
        administrative_area_level_4 = 'administrative_area_level_4', _('Administrative Area Level 4')
        administrative_area_level_5 = 'administrative_area_level_5', _('Administrative Area Level 5')

    code = models.IntegerField(null=True)
    name = models.CharField(max_length=120)
    flag = models.ImageField(upload_to=RandomFileName('locations/images/'))
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    type = models.CharField(max_length=60, choices=Types.choices, default=Types.locality)
    bounds = JSONField(null=True, blank=True, validators=[JSONSchemaValidator(limit_value=schema_location_area_bound)])

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='locations')

    # Zoom
    zoom_desktop = models.IntegerField(default=14)
    zoom_mobile = models.IntegerField(default=13)

    # Google data
    google_map_key = CICharField(max_length=150, unique=True)
    geo_code_json = JSONField(null=True, blank=True)

    class Meta:
        """Meta options."""
        ordering = ('name',)
        unique_together = [['country', 'code']]

    def __str__(self):
        return f'{self.name} is a location of {self.country}'


class LanguageCode(CitixenModel):
    """LanguageCode model."""

    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=120, unique=True)

    class Meta:
        """Meta options."""
        ordering = ('code',)

    def __str__(self):
        return f'{self.code} - {self.name}'
