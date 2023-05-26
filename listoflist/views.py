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
#from .permissions import IsAdminOrReadOnly



class cityListeCreateView(generics.ListCreateAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    #permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = cityserializer(queryset, many=True, context={'request': request})
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No city found'}, status=status.HTTP_404_NOT_FOUND)
        
class citydetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    liikup_field = 'id' # slug
    #permission_classes = [IsAdminOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No city Found'}, status=status.HTTP_404_NOT_FOUND)