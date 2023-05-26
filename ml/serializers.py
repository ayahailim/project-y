from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import classifier
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers

class classifierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = classifier
        fields = ('image','date','user', 'prediction')
        read_only_fields = ('user', 'prediction')
