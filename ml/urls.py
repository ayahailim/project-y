
from ml import views
from .views import classAPIView
from django.urls import path

urlpatterns = [
    
    path('api/predict_disease/', classAPIView.as_view(), name='predict the disease'),
]