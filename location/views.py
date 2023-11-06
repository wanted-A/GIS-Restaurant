from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from location.models import Location
from location.serializers import LocationSerializer


# GET api/v1/restaurants/location/
class LocationListAPIView(APIView):
    
    def get(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)