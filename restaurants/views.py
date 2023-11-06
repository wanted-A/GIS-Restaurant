from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantSerializer

# from haversine import haversine
import math


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


# 하버사인 공식을 활용해 직접 거리 구하기
# 참고 블로그: https://kayuse88.github.io/haversine/
def get_haversine_distance(user_point, restaurant_point):
    earth_radius = 6371

    user_lat = user_point[0]
    user_lon = user_point[1]
    restaurant_lat = restaurant_point[0]
    restaurant_lon = restaurant_point[1]

    lat_radian = math.radians(abs(user_lat - restaurant_lat))
    lon_radian = math.radians(abs(user_lon - restaurant_lon))

    lat_radian_sin = math.sin(lat_radian / 2)
    lon_radian_sin = math.sin(lon_radian / 2)

    square_root = math.sqrt(
        (lat_radian_sin * lon_radian_sin)
        + (
            math.cos(math.radians(user_lat))
            * math.cos(math.radians(restaurant_lat))
            * lat_radian_sin
            * lon_radian_sin
        )
    )

    distance = 2 * earth_radius * math.asin(square_root)

    return distance


# GET api/v1/restaurants/list
class RestaurantListAPIView(APIView):
    def get(self, request):
        user_lat = request.query_params.get("lat")
        user_lon = request.query_params.get("lon")
        range = request.query_params.get("range")
        if (user_lat is None) or (user_lon is None) or (range is None):
            return Response(
                {"message": "필수값을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        user_point = (float(user_lat), float(user_lon))
        range = float(range)

        sort_type = request.query_params.get("sort_type")
        if sort_type is None:
            sort_type = "거리순"

        restaurants = Restaurant.objects.all()
        restaurant_with_distance = []
        for restaurant in restaurants:
            restaurant_point = (restaurant.latitude, restaurant.longitude)

            distance = get_haversine_distance(user_point, restaurant_point)
            # distance = haversine(user_point, restaurant_point)
            if distance <= range:
                print(
                    f"{restaurant},{distance},{restaurant.latitude},{restaurant.longitude},{restaurant.business_status_name}"
                )
                restaurant_with_distance.append((restaurant, distance))

        if sort_type == "거리순":
            restaurant_with_distance = sorted(
                restaurant_with_distance, key=lambda x: x[1]
            )
        else:
            restaurant_with_distance = sorted(
                restaurant_with_distance, key=lambda x: x[0].rating
            )

        restaurant_list = [
            restaurant_data[0] for restaurant_data in restaurant_with_distance
        ]

        serializer = RestaurantSerializer(restaurant_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
