from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics

from rest_framework import viewsets
from .models import *
from .serializers import *

from datetime import datetime, timedelta
from django.db.models import Q, F
import json

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

  @action(detail=False, methods=['POST',], name='Create Exit Record')
  def createExitRecord(self, request):
    requestData = request.data
    record = VenueEntryExitRecord.objects.filter(
        hkuMember = HKUMember.objects.get(HKUID=requestData["hkuMember"]),
        venue = Venue.objects.get(venueCode=requestData["venue"]),
        exitDatetime = None)
    recordID = record[0].id
    entryDatetime = record[0].entryDatetime
    record.update(
      exitDatetime=requestData["exitDatetime"], 
      duration = datetime.strptime(requestData["exitDatetime"], "%Y-%m-%d %H:%M:%S%z") - entryDatetime)
    
    venue_serializer = VenueEntryExitRecordSerialization(VenueEntryExitRecord.objects.get(id=recordID))
    return Response(venue_serializer.data)

  @action(
    detail=False, 
    methods=['GET',],
    url_path=r'getCloseContacts/(?P<hkuid>\w+)/(?P<date>[0-9.,:+-]+)', 
    url_name="Close contacts", 
    name='Get close contacts')
  def getCloseContacts(self, request, hkuid=None, date=None):
    closeContacts = []
    records = VenueEntryExitRecord.objects.filter(
        hkuMember = HKUMember.objects.get(HKUID=hkuid),
        entryDatetime__range=[
          datetime.strptime(date, "%Y-%m-%d%z") - timedelta(days=3), datetime.strptime(date, "%Y-%m-%d%z")],
          duration__gte = timedelta(minutes=30))
    
    for record in records:
      closeContactsForThisRecord = VenueEntryExitRecord.objects.filter(
                        ~Q(hkuMember =record.hkuMember.HKUID),
                        venue=record.venue.venueCode,
                        entryDatetime__gte = record.entryDatetime,
                        exitDatetime__lte = record.exitDatetime,
                        duration__gte = timedelta(minutes=30)) | \
                      VenueEntryExitRecord.objects.filter(
                        ~Q(hkuMember =record.hkuMember.HKUID),
                        venue=record.venue.venueCode,
                        entryDatetime__lte = record.entryDatetime,
                        exitDatetime__lte = record.exitDatetime,
                        exitDatetime__gte = record.entryDatetime + timedelta(minutes=30)) | \
                      VenueEntryExitRecord.objects.filter(
                        ~Q(hkuMember =record.hkuMember.HKUID),
                        venue=record.venue.venueCode,
                        entryDatetime__gte = record.entryDatetime,
                        exitDatetime__gte = record.exitDatetime,
                        entryDatetime__lte = record.exitDatetime + timedelta(minutes=30)) | \
                      VenueEntryExitRecord.objects.filter(
                        ~Q(hkuMember =record.hkuMember.HKUID),
                        venue=record.venue.venueCode,
                        entryDatetime__lte = record.entryDatetime,
                        exitDatetime__gte = record.exitDatetime)
      for closeContact in closeContactsForThisRecord:
        closeContacts.append({'HKUID': closeContact.hkuMember.HKUID , 'name': HKUMember.objects.filter(HKUID=closeContact.hkuMember.HKUID)[0].name})
    
    seen = set()
    removeDuplicateCloseContacts = []
    for d in closeContacts:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            removeDuplicateCloseContacts.append(d)

    return Response(removeDuplicateCloseContacts)

  @action(
    detail=False, methods=['GET',], 
    url_path=r'getVisitedVenues/(?P<hkuid>\w+)/(?P<date>[0-9.,:+-]+)', 
    url_name="visited venues", 
    name='Get visited venues'
  )
  def getVisitedVenues(self, request, hkuid=None, date=None):
    visitedVenuesCode = []

    record = VenueEntryExitRecord.objects.filter(
        hkuMember = HKUMember.objects.get(HKUID=hkuid),
        entryDatetime__range=[
          datetime.strptime(date, "%Y-%m-%d%z") - timedelta(days=3), datetime.strptime(date, "%Y-%m-%d%z")])

    venue_serializer = VenueCodeOnlyVenueEntryExitRecordSerialization(record, many=True)
    return Response(venue_serializer.data)