from accounts import views
from .views import RegisterAPI,LoginAPI ,UpdateUser ,ChangePasswordView
from knox import views as knox_views
from django.urls import path

urlpatterns = [
    path('signup/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('updateprofile/', UpdateUser.as_view(), name='updateprofile'), 
    path('ChangePassword/', ChangePasswordView.as_view(), name='ChangePassword'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),



    
]

    