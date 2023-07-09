from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
# Create your views here.
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

'''class TaskList(generics.ListCreateAPIView):
    
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Task.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if self.request.query_params.get('title'):
            queryset = queryset.filter(title__icontains=self.request.query_params.get('title'))
        return queryset'''
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if self.request.query_params.get('title'):
            queryset = queryset.filter(title__icontains=self.request.query_params.get('title'))
        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)


'''class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [JSONRenderer]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        instance.delete()
        response = Response({'success': 'Object deleted.'}, status=200)
        response['Cache-Control'] = 'no-cache'
        return response'''