from django.urls import path
from . import views
urlpatterns = [
  
    #path('api/doctorslist/', doctorListAPIView.as_view(), name='list-of-doctors'),
    
    path("city_list/", views.cityListeCreateView.as_view(), name="city_list"),
    path("city_detail/<int:pk>/", views.citydetailView.as_view(), name="city_detail"),

]