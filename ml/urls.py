
from ml import views
from .views import classAPIView,classAPIViewtf
from django.urls import path

urlpatterns = [
    
    path('predict/', classAPIView.as_view(), name='predict the disease'),
    path('predict/<int:pk>/', classAPIView.as_view(), name='delete the disease'),
    path('predicttf/', classAPIViewtf.as_view(), name='predict the disease')
]