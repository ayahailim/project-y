
from ml import views
from .views import classifierAPIView,classAPIView
from django.urls import path

urlpatterns = [
    path('api/ml/', classifierAPIView.as_view(), name='skinscanner'),
    path('api/class/', classAPIView.as_view(), name='skinscanner'),
]