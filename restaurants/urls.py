from django.urls import path

from restaurants.views import RestaurantAPIView

urlpatterns = [
    path("<int:restaurant_id>/", RestaurantAPIView.as_view(), name="restaurant-detail"),
]
