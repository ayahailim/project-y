import dataclasses
from django.db import DataError
from rest_framework import serializers
from .models import doctor, city


class doctorserializer(serializers.ModelSerializer):
    city = serializers.CharField()
    class Meta:
        model = doctor
        fields = ('dr_name','dr_adress','dr_phone_number' ,'city')

class cityserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    city_name = serializers.CharField()
    doctors= doctorserializer(many=True, read_only=True)
    
    class Meta:
        model = city
        fields = "__all__"

