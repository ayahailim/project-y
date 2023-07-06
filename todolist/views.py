from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
# Create your views here.
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)