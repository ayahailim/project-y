from django.urls import path
from . import views
urlpatterns = [

    path("api/city/<int:pk>/", views.citydetailView.as_view(), name="city_detail"),

]