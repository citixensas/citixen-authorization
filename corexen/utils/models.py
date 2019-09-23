"""Citixen utilities."""

from django.db import models


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
