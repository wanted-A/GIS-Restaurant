from django.urls import path

from ratings.views import ReviewAPIView

urlpatterns = [
    path("<int:restaurant_id>/review/", ReviewAPIView.as_view(), name="review-create"),
]
