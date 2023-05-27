from django.urls import path
from . import views
urlpatterns = [

    path("api/doctors/<int:pk>/", views.citydetailView.as_view(), name="city_detail"),

]