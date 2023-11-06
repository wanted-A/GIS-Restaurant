from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/restaurants/", include("restaurants.urls")),
    path("api/v1/ratings/", include("ratings.urls")),
    path("api/v1/location/", include("location.urls")),
]
