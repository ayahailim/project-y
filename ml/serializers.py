from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import preuser
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers


class preuserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = preuser
        fields = ('id','image','date','prediction')
        read_only_fields = ('id', 'prediction')