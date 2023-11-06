from django.urls import path

from restaurants.views import (
    RestaurantAPIView,
    RestaurantDetailAPIView,
    RestaurantListAPIView,
)

urlpatterns = [
    path("<int:restaurant_id>/", RestaurantAPIView.as_view(), name="restaurant-info"),
    path(
        "detail/<int:restaurant_id>/",
        RestaurantDetailAPIView.as_view(),
        name="restaurant-detail",
    ),
    path("list/", RestaurantListAPIView.as_view(), name="restaurant_list"),
]
