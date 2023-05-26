from django.contrib import admin

# Register your models here.
from .models import doctor ,city

admin.site.register(doctor)

admin.site.register(city)