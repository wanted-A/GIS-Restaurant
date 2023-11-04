from rest_framework import serializers

from ratings.models import Rating
from restaurants.models import Restaurant
from users.models import User

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ["id", "user" ,"restaurant", "score", "content", "created_at", "updated_at"]