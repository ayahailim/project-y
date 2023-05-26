from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
    user=models.OneToOneField(User, related_name='userprofile',on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to="profile_pic/UserProfile/",blank=True)
    mobile = models.CharField(max_length=11,null=False)
   

    def __str__(self):
        return self.user.username
    

 