from django.db import models
from django.contrib.auth.models import User

class classifier(models.Model):
    user=models.ForeignKey(User, related_name='user_prediction',on_delete=models.CASCADE)
    image= models.ImageField(upload_to="ml/image/",blank=True)
    date =models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100,null=False)
    def __str__(self):
        return f"{self.user.username}'s image"








 