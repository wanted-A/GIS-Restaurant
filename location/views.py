from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache

from location.serializers import LocationSerializer


# GET api/v1/restaurants/location/
class LocationListAPIView(APIView):
    def get(self, request):
        """
        여기는 캐시가 존재하면 인기 맛집 장소 캐시를 반환
        """
        cache_key = "popular_location_data"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # 캐싱 되었으면 캐시 반환
            return Response(cached_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "location 에서 에러 발생: 캐싱된 데이터가 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            # # 캐싱 안 되었을 경우엔 DB에서 조회
            # from location.models import Location

            # VIEWS_THRESHOLD = 100
            # queryset = Location.objects.filter(views__gte=VIEWS_THRESHOLD)
            # serializer = LocationSerializer(queryset, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
