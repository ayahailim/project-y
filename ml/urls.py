
from ml import views
from .views import classAPIView,classAPIViewtf
from django.urls import path

urlpatterns = [
    
    path('predict/', classAPIView.as_view(), name='predict the disease'),
    path('predict/<int:id>/', classAPIView.as_view(), name='retrieve or delete a specific operation'),
    path('predicttf/', classAPIViewtf.as_view(), name='predict the disease')
]