from django.urls import path
from . import views
urlpatterns = [

    path("api/feedback/", views.FeedbackListCreateAPIView.as_view(), name="user feedback"),
    #path("api/feedback_update_destroy/", views.FeedbackListRetrieveUpdateDestroyAPIView.as_view(), name="user feedback"),
]