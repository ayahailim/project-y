from django.urls import path
from . import views
urlpatterns = [

    path("city/<int:pk>/", views.citydetailView.as_view(), name="city_detail"),

]