from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from location.models import Location
from location.serializers import LocationSerializer

from django.core.cache import cache

# GET api/v1/restaurants/location/
class LocationListAPIView(APIView):
    
    def get(self, request):

        # cache에 저장된 데이터가 없을 경우 실행
        if not cache.get('location_data'):
            queryset = Location.objects.all()
            serializer = LocationSerializer(queryset, many=True)
            cache.set('location_data', serializer.data)
            
        data = cache.get('location_data')
        return Response(data, status=status.HTTP_200_OK)