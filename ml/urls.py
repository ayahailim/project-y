
from ml import views
from .views import classAPIViewtf
from django.urls import path

urlpatterns = [
    
    path('predict/<int:id>/', classAPIViewtf.as_view(), name='retrieve or delete a specific operation'),
    path('predict/', classAPIViewtf.as_view(), name='predict the disease'),
    
]