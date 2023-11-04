from rest_framework import serializers
from ratings.serializers import RatingListSerializer
from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "location_name",
            "location_code",
            "restaurant_name",
            "license_date",
            "business_status_name",
            "closed_date",
            "location_area",
            "water_supply_facility_name",
            "male_worker_count",
            "year",
            "multi_use_yn",
            "grade_division_name",
            "total_facility_scale",
            "female_worker_count",
            "business_site_around_name",
            "clean_industry_name",
            "clean_business_type",
            "total_worker_count",
            "road_address",
            "lot_num_address",
            "zip_code",
            "latitude",
            "longitude",
            "rating",
            "restaurant_code",
            "reviews"
        ]
    
    def get_reviews(self, obj):
        restaurant = Restaurant.objects.get(id=obj.id)
        # 리뷰는 최신순으로 5개까지만 반환하도록 한다.
        review_list = restaurant.restaurant_ratings.all().order_by("-created_at")[:5]
        return RatingListSerializer(review_list, many=True).data