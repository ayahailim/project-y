
from ml import views
from .views import classAPIView
from django.urls import path

urlpatterns = [
    
    path('predict/', classAPIView.as_view(), name='predict the disease'),
]