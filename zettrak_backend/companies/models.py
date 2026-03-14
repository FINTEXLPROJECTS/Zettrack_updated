from django.db import models

# Create your models here.
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name