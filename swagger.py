from rest_framework import serializers
from drf_yasg import openapi

from users.models import User


# Parameters
QUERY_LAT = openapi.Parameter(
    "lat",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="사용자 위도",
    required=True,
)

QUERY_LON = openapi.Parameter(
    "lon",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="사용자 경도",
    required=True,
)

QUERY_RANGE = openapi.Parameter(
    "range",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="검색 범위, 단위는 km",
    required=True,
)

QUERY_SORT_TYPE = openapi.Parameter(
    "sort_type",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="정렬 타입, 거리순 또는 평점순, 현재는 오름차순만 구현",
    default="거리순",
)

PATH_RESTAURANT_ID = openapi.Parameter(
    "restaurant_id",
    openapi.IN_PATH,
    type=openapi.TYPE_INTEGER,
    description="맛집 고유번호",
    required=True,
)

PATH_RESTAURANT_ID_NOT_REQUIRED = openapi.Parameter(
    "restaurant_id",
    openapi.IN_PATH,
    type=openapi.TYPE_INTEGER,
    description="맛집 고유번호",
)


class SwaggerSignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class SwaggerSignupResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "is_recommend"]


class SwaggerLoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
