from accounts import views
from .views import RegisterAPI,LoginAPI ,UpdateUser ,ChangePasswordView
from knox import views as knox_views
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/updateprofile/', UpdateUser.as_view(), name='updateprofile'), 
    path('api/ChangePassword/', ChangePasswordView.as_view(), name='ChangePassword'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),



    
]

    