"""Citixen utilities."""
import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


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
