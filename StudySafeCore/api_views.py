from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from rest_framework import viewsets
from .models import *
from .serializers import *

# @api_view(['GET',])
# def list_all_venues(request):
#   venues = Venue.objects.all()
#   venue_serializer = VenueSerialization(venues, many=True)
#   return Response(venue_serializer.data)


# class list_all_venues(generics.ListAPIView):
#   queryset = Venue.objects.all()
#   serializer_class = VenueSerialization

class VenueViewSet(viewsets.ModelViewSet):
  lookup_value_regex = '[^/]+'
  queryset = Venue.objects.all()
  serializer_class = VenueSerialization
  # lookup_field = 'pk'

  # def retrieve(self, request, pk=None):
  #   queryset = Venue.objects.get(venueCode=pk)
  #   # venue = get_object_or_404(queryset, pk=pk)
  #   serializer = VenueSerialization(queryset)
  #   return Response(serializer.data)

class MemberViewSet(viewsets.ModelViewSet):
  queryset = HKUMember.objects.all()
  serializer_class = MemberSerialization

class EntryExitRecordViewSet(viewsets.ModelViewSet):
  queryset = VenueEntryExitRecord.objects.all()
  serializer_class = VenueEntryExitRecordSerialization