from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from ratings.serializers import RatingListSerializer

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


# GET api/v1/restaurants/<int:restaurant_id>/
class RestaurantAPIView(APIView):

    def get_object(self, restaurant_id):
        try:
            return Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound("해당 맛집을 찾을 수 없습니다.")


    def get(self, request, restaurant_id):
        restaurant = self.get_object(restaurant_id)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

