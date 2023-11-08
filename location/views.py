from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from location.serializers import LocationSerializer
from location.models import Location

from swagger import *


# GET api/v1/location/
# Redis 적용 전: 54ms
# Redis 적용 후: 16ms
class LocationListAPIView(APIView):
  
    @swagger_auto_schema(
        operation_id="시군구 목록 조회",
        operation_description="음식점 데이터에 사용되는 시군구의 목록을 조회할 수 있습니다.",
        responses={200: LocationSerializer},
    )
    def get(self, request):
        # 캐싱된 데이터가 있는지 확인
        location_data = cache.get("location/")

        # 지역 데이터가 캐싱되어 있을 경우
        if location_data:
            # 캐싱된 데이터를 반환
            return Response(location_data, status=status.HTTP_200_OK)

        # 지역 데이터가 캐싱되어 있지 않을 경우
        location_data = Location.objects.all()

        # 데이터를 직렬화한 다음 캐싱
        serializer = LocationSerializer(location_data, many=True)
        # 장시간 변동이 없는 데이터, 만료기간 설정 X
        cache.set("location/", serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
