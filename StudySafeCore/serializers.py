# from rest_framework import serializers
from StudySafeCore.models import *
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

class MemberSerialization(serializers.ModelSerializer):
  class Meta:
    model = HKUMember
    fields = '__all__'

class VenueEntryExitRecordSerialization(serializers.ModelSerializer):
  class Meta:
    model = VenueEntryExitRecord
    fields = '__all__'