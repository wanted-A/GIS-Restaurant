from django.urls import path
from .views import TestAPIView

urlpatterns = [
    path("test/", TestAPIView.as_view()),
]
