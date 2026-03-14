from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active_employee = models.BooleanField(default=True)

    def __str__(self):
        return self.username