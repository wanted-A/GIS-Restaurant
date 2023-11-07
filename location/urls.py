from django.urls import path

from location.views import LocationListAPIView

urlpatterns = [
    path("", LocationListAPIView.as_view(), name="location-list"),
]
