"""Company model"""

from django.db import models


class Company(models.Model):
    """Company model."""

    nit = models.CharField(max_length=50)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    country = models.CharField(max_length=30)  # El tipo de campo es temporal, deberá ser una relación a países
    #created_by = test_models.ForeignKey('users.User', on_delete=test_models.CASCADE, related_name='company_created_by')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
