# from rest_framework import serializers

# class MembersSerializer(serializers.Serializer):
#     #id = serializers.IntegerField(read_only = True)
#     HKUID = serializers.CharField(max_length=10, read_only = True)
#     name = serializers.CharField(max_length=150)

from StudySafeCore.models import Venue
from rest_framework import serializers

# class VenueSerialization(serializers.Serializer):
#   venueCode = serializers.CharField(max_length=20)
#   location = serializers.CharField(max_length=150)
#   type = serializers.CharField(max_length=3)
#   capacity = serializers.IntegerField()

class VenueSerialization(serializers.ModelSerializer):

  class Meta:
    model = Venue
    fields = '__all__'