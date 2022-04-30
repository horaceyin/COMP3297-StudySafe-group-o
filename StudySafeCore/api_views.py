from curses import reset_prog_mode
from modulefinder import ReplacePackage
# from selectors import EpollSelector
from sre_constants import SUCCESS

from django.http import Http404
from itsdangerous import Serializer

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, status

from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *

from datetime import datetime, timedelta
from django.db.models import Q, F
import json

class VenueViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[^/]+'
    queryset = Venue.objects.all()
    serializer_class = VenueSerialization


class MemberViewSet(viewsets.ModelViewSet):
    queryset = HKUMember.objects.all()
    serializer_class = HKUMemberSerialization


class VenueEntryExitRecordViewSet(viewsets.ModelViewSet):
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = VenueEntryExitRecordSerialization  # default serializer

    # override get_serializer_class to set a different serializer
    # def get_serializer_class(self):
    #     return self.serializer_classes.get(self.action, self.serializer_class)

    # def create(self, request, *args, **kwargs):
    #     serializer = VenueEntrySerialization(data=request.data)
    #     print(serializer.is_valid())
    #     if serializer.is_valid():
    #         response = super(EntryExitRecordViewSet, self).create(
    #             request, *args, **kwargs)
    #         response.data = {'id': response.data['id']}
    #         return Response(response.data, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # @action(detail=False, methods=['POST', ], name='Create Exit Record')
    # def createExitRecord(self, request):
    #     valid = True
    #     record = VenueEntryExitRecord.objects.filter(
    #             hkuMember=HKUMember.objects.get(
    #             HKUID=request.data["hkuMember"]),
    #             venue=Venue.objects.get(venueCode=request.data["venue"]),
    #             exitDatetime=NULL).order_by('-entryDatetime')[0]

    #     if record is None:
    #         #The relevant entry record cannot be found
    #         valid = False
    #         pass

    #     if request.data["exitDatetime"] < record.entryDatetime:
    #         #the exit time is earlier than the entry time
    #         valid = False
    #         pass
        
    #     if valid:
    #         record.update(
    #             exitDatetime=request.data["exitDatetime"],
    #             duration=datetime.strptime(request.data["exitDatetime"], "%Y-%m-%d %H:%M:%S%z") - record.entryDatetime)
    #         response = {'id': record.id}
    #         return Response(response, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(
        detail=False,
        methods=['GET', ],
        url_path=r'getCloseContacts/(?P<hkuid>\w+)/(?P<date>[0-9.,:+-]+)',
        url_name="Close contacts",
        name='Get close contacts')
    def getCloseContacts(self, request, hkuid=None, date=None):
        closeContacts = []
        records = VenueEntryExitRecord.objects.filter(
            hkuMember=HKUMember.objects.get(HKUID=hkuid),
            entryDatetime__range=[
                datetime.strptime(date, "%Y-%m-%d%z") - timedelta(days=2), datetime.strptime(date, "%Y-%m-%d%z")],
            duration__gte=timedelta(minutes=30))

        for record in records:
            closeContactsForThisRecord = VenueEntryExitRecord.objects.filter(
                ~Q(hkuMember=record.hkuMember.HKUID),
                venue=record.venue.venueCode,
                entryDatetime__gte=record.entryDatetime,
                exitDatetime__lte=record.exitDatetime,
                duration__gte=timedelta(minutes=30)) | \
                VenueEntryExitRecord.objects.filter(
                ~Q(hkuMember=record.hkuMember.HKUID),
                venue=record.venue.venueCode,
                entryDatetime__lte=record.entryDatetime,
                exitDatetime__lte=record.exitDatetime,
                exitDatetime__gte=record.entryDatetime + timedelta(minutes=30)) | \
                VenueEntryExitRecord.objects.filter(
                ~Q(hkuMember=record.hkuMember.HKUID),
                venue=record.venue.venueCode,
                entryDatetime__gte=record.entryDatetime,
                exitDatetime__gte=record.exitDatetime,
                entryDatetime__lte=record.exitDatetime + timedelta(minutes=30)) | \
                VenueEntryExitRecord.objects.filter(
                ~Q(hkuMember=record.hkuMember.HKUID),
                venue=record.venue.venueCode,
                entryDatetime__lte=record.entryDatetime,
                exitDatetime__gte=record.exitDatetime)
            for closeContact in closeContactsForThisRecord:
                closeContacts.append({'HKUID': closeContact.hkuMember.HKUID, 'name': HKUMember.objects.filter(
                    HKUID=closeContact.hkuMember.HKUID)[0].name})

        seen = set()
        removeDuplicateCloseContacts = []
        for d in closeContacts:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                removeDuplicateCloseContacts.append(d)

        return Response(removeDuplicateCloseContacts)

    @action(
        detail=False, methods=['GET', ],
        url_path=r'getVisitedVenues/(?P<hkuid>\w+)/(?P<date>[0-9.,:+-]+)',
        url_name="visited venues",
        name='Get visited venues'
    )
    def getVisitedVenues(self, request, hkuid=None, date=None):
        visitedVenuesCode = []

        record = VenueEntryExitRecord.objects.filter(
            hkuMember=HKUMember.objects.get(HKUID=hkuid),
            entryDatetime__range=[
                datetime.strptime(date, "%Y-%m-%d%z") - timedelta(days=2), datetime.strptime(date, "%Y-%m-%d%z")])

        venue_serializer = VenueCodeOnlyVenueEntryExitRecordSerialization(
            record, many=True)
        return Response(venue_serializer.data)

class ExitRecordView(generics.GenericAPIView):
    
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = ExitSerialization

    def getInstanceByUidVenue(self,uid,venue):
        queryset = VenueEntryExitRecord.objects.filter(
            hkuMember=HKUMember.objects.get(
            HKUID=uid),
            venue=Venue.objects.get(venueCode=venue),
            exitDatetime=None).order_by('-entryDatetime')
        if queryset:
            return queryset[0]
        else:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        try:
            instance = self.getInstanceByUidVenue(request.data["hkuMember"],request.data["venue"])
        except:
            return Response({"non_field_errors": ["Invalid! There is no unclosed entry record for this member at this venue!"]},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExitSerialization(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class EntryRecordView(generics.CreateAPIView):
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = EntryRecordSerialization

    def create(self, request, *args, **kwargs):
        serializer = EntryRecordSerialization(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            # response
            # # print(dir(serializer))
            # print(serializer.data)
            # serializer = VenueEntryExitRecordSerialization(response)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)