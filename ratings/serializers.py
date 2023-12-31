from rest_framework import serializers

from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ["id", "user" ,"restaurant", "score", "content", "created_at", "updated_at"]


class RatingListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ["id", "user" ,"restaurant", "score", "content", "created_at", "updated_at"]

    def to_representation(self, instance):
        # content 최대 20자 까지만 표현
        res = super().to_representation(instance)
        if res and len(res["content"]) > 20:
            res.update({'content': res['content'][:20]})
        return res
