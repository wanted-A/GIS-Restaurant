from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.core.cache import cache

from location.serializers import LocationSerializer


# GET api/v1/location/
# Redis 적용 전: 54ms
# Redis 적용 후: 16ms
class LocationListAPIView(APIView):
    def get(self, request):
        location = cache.get("location_data")
        serializer = LocationSerializer(location, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
