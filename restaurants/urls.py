from django.urls import path

from restaurants.views import LocationListAPIView, RestaurantAPIView, RestaurantDetailAPIView

urlpatterns = [
    path("<int:restaurant_id>/", RestaurantAPIView.as_view(), name="restaurant-info"),
    path("detail/<int:restaurant_id>/", RestaurantDetailAPIView.as_view(), name="restaurant-detail"),

    path("location/", LocationListAPIView.as_view(), name="location-list"),
]
