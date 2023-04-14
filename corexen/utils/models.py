"""Citixen utilities."""
import json
import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.db import models
from django.utils import timezone


class JSONField(models.JSONField):
    pass

if 'sqlite' in settings.DATABASES['default']['ENGINE']:
    class JSONField(models.TextField):
        def to_python(self, value):
            if value is not None:
                try:
                    return json.loads(value)
                except (TypeError, ValueError):
                    return value
            return value

        def get_prep_value(self, value):
            if value is not None:
                return str(json.dumps(value))
            return value

        def value_to_string(self, obj):
            return self.value_from_object(obj)


class CitixenModel(models.Model):
    """Citixen base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        abstract = True
        ordering = ('-created_at', '-updated_at')

    def update(self, *args, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


class ParanoidQuerySet(models.QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            obj.save()


class ParanoidManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoidQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class ParanoidModel(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = ParanoidManager()
    original_objects = models.Manager()

    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
