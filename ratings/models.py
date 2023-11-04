from django.db import models
from restaurants.models import Restaurant
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ratings", blank=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_ratings", blank=False)
    score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    content = models.TextField(max_length=255, blank=True, null=True)