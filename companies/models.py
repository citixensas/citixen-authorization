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


class Headquarter(models.Model):
    """Headquarter model."""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    name = models.CharField(max_length=120)

    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=120)
    neighborhood = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    recruitment = models.BooleanField(default=False)
    recruitment_message = models.CharField(max_length=250, blank=True, null=True)

    created_by = models.UUIDField(null=True)
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
