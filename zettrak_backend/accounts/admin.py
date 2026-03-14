from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Role

admin.site.register(User)
admin.site.register(Role)