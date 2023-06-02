from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    message = models.TextField()
    stars = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=1.0)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.name