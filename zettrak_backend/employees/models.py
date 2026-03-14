from django.db import models
from accounts.models import User
from companies.models import Company


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_code = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name