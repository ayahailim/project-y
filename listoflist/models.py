from django.db import models
from django.template.defaultfilters import slugify
import random
import string

# Create your models here.
class city(models.Model):
    city_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.city_name

class doctor(models.Model):
    dr_name = models.CharField(max_length=20)
    dr_adress = models.CharField(max_length=20)
    dr_phone_number = models.CharField(max_length=11)
    city = models.ForeignKey(city, related_name= 'doctors', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.dr_name

    