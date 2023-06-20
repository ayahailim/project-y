from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import city, doctor
from .serializers import cityserializer, doctorserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

'''class cityListeCreateView(generics.ListCreateAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = cityserializer(queryset, many=True, context={'request': request})
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No city found'}, status=status.HTTP_404_NOT_FOUND)'''
        
class citydetailView(generics.RetrieveAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    permission_classes = [IsAdminOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No city Found'}, status=status.HTTP_404_NOT_FOUND)