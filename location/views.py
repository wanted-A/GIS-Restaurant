from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from location.models import Location
from location.serializers import LocationSerializer

from swagger import *


# GET api/v1/restaurants/location/
class LocationListAPIView(APIView):
    @swagger_auto_schema(
        operation_id="시군구 목록 조회",
        operation_description="음식점 데이터에 사용되는 시군구의 목록을 조회할 수 있습니다.",
        responses={200: LocationSerializer},
    )
    def get(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
