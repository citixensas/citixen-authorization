"""Company model"""

from django.db import models


class Company(models.Model):
    """Company model."""

    nit = models.CharField(max_length=50)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    country = models.CharField(max_length=30)  # This will be a relationship

    is_active = models.BooleanField(default=False)

    created_by = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
