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
    dr_description = models.CharField(max_length=200)
    city = models.ForeignKey(city, related_name= 'city', on_delete=models.SET_NULL, null=True)
    slug = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.dr_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.dr_name + " " + self.dr_adress + " " + self.city.city_name)
            self.slug = base_slug + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        return super().save(*args, **kwargs)