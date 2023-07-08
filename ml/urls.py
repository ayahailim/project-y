
from ml import views
from .views import classAPIView,classAPIViewtf
from django.urls import path

urlpatterns = [
    
    path('predicth/', classAPIView.as_view(), name='predict the disease'),
    path('predict/<int:id>/', classAPIView.as_view(), name='retrieve or delete a specific operation'),
    path('predict/', classAPIViewtf.as_view(), name='predict the disease'),
    
]