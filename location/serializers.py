from rest_framework import serializers

from location.models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ["id", "do_si", "sgg", "latitude", "longitude"]