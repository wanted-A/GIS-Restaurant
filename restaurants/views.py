from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantSerializer

from swagger import *

import os
import environ
import requests
import json

import math


env = environ.Env()
env_file = os.path.join(os.path.dirname(__file__), ".env")
env.read_env(env_file)


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

    @swagger_auto_schema(
        operation_id="맛집 상세정보(간략한 데이터)",
        operation_description="맛집에 대한 상세 정보 중 중요한 데이터만 제공합니다.",
        manual_parameters=[PATH_RESTAURANT_ID],
        responses={
            200: RestaurantSerializer,
            400: "```{\ndetail: 해당 맛집을 찾을 수 없습니다.",
        },
    )
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

    @swagger_auto_schema(
        operation_id="맛집 상세정보",
        operation_description="맛집에 대한 상세정보를 제공합니다.",
        manual_parameters=[PATH_RESTAURANT_ID],
        responses={
            200: RestaurantDetailSerializer,
            400: "```{\ndetail: 해당 맛집을 찾을 수 없습니다.",
        },
    )
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


# 구글 역 지오코딩 활용하여 지역명 산출
def get_reverse_geocoding(user_point):
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    parameters = {
        "latlng": f"{user_point[0]},{user_point[1]}",
        "key": env("LOCATION_API_KEY"),
        "language": "ko",
        "result_type": "locality",
    }

    try:
        response = (
            json.loads(requests.get(url, params=parameters).text)["results"][0]
            .get("address_components")[0]
            .get("long_name")
        )
        return response
    except Exception as e:
        print(e)


# GET api/v1/restaurants/list
class RestaurantListAPIView(APIView):
    """
    맛집 목록(위치 기반)
    """

    @swagger_auto_schema(
        operation_id="맛집 목록",
        operation_description="사용자 위치로부터 일정 범위 내에 위치하는 맛집 목록을 제공합니다.",
        manual_parameters=[
            QUERY_LAT,
            QUERY_LON,
            QUERY_RANGE,
            QUERY_SORT_TYPE,
        ],
        responses={
            200: RestaurantSerializer,
            400: "```{\nmessage: 필수값을 입력해주세요.",
            404: "```{\nmessage: 해당 조건에 일치하는 음식점이 없습니다.",
        },
    )
    def get(self, request):
        user_lat = request.query_params.get("lat")
        user_lon = request.query_params.get("lon")
        range = request.query_params.get("range")
        # 필수 파라미터가 없을 경우 400 리턴
        if (user_lat is None) or (user_lon is None) or (range is None):
            return Response(
                {"message": "필수값을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        user_point = (float(user_lat), float(user_lon))
        range = float(range)

        sort_type = request.query_params.get("sort_type", "거리순")

        # DB에 지역명이 일치하는 데이터만 가져옴
        restaurants = Restaurant.objects.filter(
            location_name=get_reverse_geocoding(user_point)
        )

        restaurant_with_distance = []
        for restaurant in restaurants:
            restaurant_point = (restaurant.latitude, restaurant.longitude)

            # 위경도를 이용해 두 점간 거리를 산출
            distance = get_haversine_distance(user_point, restaurant_point)
            if distance <= range:
                # 거리순 정렬을 위해 음식점 객체와 거리를 묶음
                restaurant_with_distance.append((restaurant, distance))

        # sort_type에 따라 데이터 정렬
        if sort_type == "거리순":
            restaurant_with_distance = sorted(
                restaurant_with_distance, key=lambda x: x[1]
            )
        else:
            restaurant_with_distance = sorted(
                restaurant_with_distance, key=lambda x: x[0].rating
            )

        # 직렬화를 위해 음식점 객체만 리스트
        restaurant_list = [
            restaurant_data[0] for restaurant_data in restaurant_with_distance
        ]

        serializer = RestaurantSerializer(restaurant_list, many=True)
        # 조건에 일치하는 음식점이 없을 경우 serializer는 빈 리스트가 됨
        if serializer.data == []:
            return Response(
                {"message": "해당 조건에 일치하는 음식점이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
