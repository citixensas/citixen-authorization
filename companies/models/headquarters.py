"""Headquarter model"""

from django.db import models

from companies.models import Company


class Headquarter(models.Model):
    """Headquarter model."""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    neighborhood = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    #created_by = test_models.ForeignKey('users.User', on_delete=test_models.CASCADE,
    #                               related_name='headquarters_created_by')  # pylint: disable=no-name-in-module
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate_or_deactivate(self):
        self.is_active = not self.is_active
        self.save()

    def mark_as_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'{self.name} is a headquarters of {self.company.name}'
