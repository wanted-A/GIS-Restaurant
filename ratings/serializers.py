from rest_framework import serializers

from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ["id", "user" ,"restaurant", "score", "content", "created_at", "updated_at"]