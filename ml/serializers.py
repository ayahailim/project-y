from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import preuser
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
import pytz
from rest_framework import serializers
from django.utils import timezone

class EgyptDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        timezone_obj = pytz.timezone('Africa/Cairo')
        date_with_clock = timezone.localtime(value, timezone_obj)
        return date_with_clock.strftime('%Y-%m-%d %I:%M %p')

class preuserSerializer(serializers.ModelSerializer):
    date = EgyptDateTimeField()
    class Meta:
        model = preuser
        fields = ('id','image','date','prediction')
        read_only_fields = ('id', 'prediction')