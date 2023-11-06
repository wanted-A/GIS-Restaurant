from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import permissions

from restaurants.models import Location, Restaurant
from restaurants.serializers import LocationSerializer, RestaurantDetailSerializer, RestaurantSerializer


# GET api/v1/restaurants/<int:restaurant_id>/
class RestaurantAPIView(APIView):
    """
    맛집 상세정보 조회(일부 필요 정보만 조회)
    """

    def get_object(self, restaurant_id):
        try:
            return Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound("해당 맛집을 찾을 수 없습니다.")


    def get(self, request, restaurant_id):
        restaurant = self.get_object(restaurant_id)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET api/v1/restaurants/detail/<int:restaurant_id>/
class RestaurantDetailAPIView(APIView):
    """
    맛집 상세정보 조회(모든 필드 조회)
    """

    def get_object(self, restaurant_id):
        try:
            return Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound("해당 맛집을 찾을 수 없습니다.")


    def get(self, request, restaurant_id):
        restaurant = self.get_object(restaurant_id)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET api/v1/restaurants/location/
class LocationListAPIView(APIView):
    
    def get(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)