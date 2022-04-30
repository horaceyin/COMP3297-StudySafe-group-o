# from rest_framework import serializers
from StudySafeCore.models import *
from rest_framework import serializers
import datetime


class VenueSerialization(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

        def validate(self, data):
            # check Capacity is not negative
            if data['capacity'] < 0:
                raise serializers.ValidationError(
                    "Capacity of a venue cannot be negative!")
            return data


class HKUMemberSerialization(serializers.ModelSerializer):
    class Meta:
        model = HKUMember
        fields = '__all__'


class VenueEntryExitRecordSerialization(serializers.Serializer):
    class Meta:
        model = VenueEntryExitRecord
        fields = "__all__"


class VenueCodeOnlyVenueEntryExitRecordSerialization(serializers.ModelSerializer):
    class Meta:
        model = VenueEntryExitRecord

class EntryRecordSerialization(serializers.ModelSerializer):
    #use default implementation for create
    class Meta:
        model = VenueEntryExitRecord
        fields = ["hkuMember","venue","entryDatetime"]

    def validate(self, data):
        # check if the entry time is reasonably current
        currentTime = datetime.datetime.now()
        if currentTime.replace(tzinfo=None) > data["entryDatetime"].replace(tzinfo=None):
            timeDiff = currentTime.replace(tzinfo=None) - data["entryDatetime"].replace(tzinfo=None)
        else:
            timeDiff = data["entryDatetime"].replace(tzinfo=None) - currentTime.replace(tzinfo=None)
        # print(timeDiff)
        # print(timeDiff.seconds // 60)
        if abs(timeDiff.seconds // 60) > 2:
            raise serializers.ValidationError(
                "Invalid record! The system our accepts ENTRY records within 2 minutes of the current time")
        return data
    
class ExitSerialization(serializers.ModelSerializer):
    class Meta:
        model = VenueEntryExitRecord
        fields = ['hkuMember', 'venue','exitDatetime']

    def validate(self, data):
        # check if wanted entry record already has an exit time
        record = self.instance
        if record.exitDatetime is not None:
            raise serializers.ValidationError(
                "This entry record already has an exit time")
        # check if the exit time of is earlier than the entry time for this record
        if data["exitDatetime"] < record.entryDatetime:
            raise serializers.ValidationError(
                "The exit time is earlier than entry time!")
        # check if the exit time is reasonably current
        currentTime = datetime.datetime.now()
        if currentTime.replace(tzinfo=None) > data["exitDatetime"].replace(tzinfo=None):
            timeDiff = currentTime.replace(tzinfo=None) - data["exitDatetime"].replace(tzinfo=None)
        else:
            timeDiff = data["exitDatetime"].replace(tzinfo=None) - currentTime.replace(tzinfo=None)
        if abs(timeDiff.seconds // 60) > 2:
            print("FUCK")
            raise serializers.ValidationError("Invalid record! The system our accepts EXIT records within 2 minutes of the current time")
        return data