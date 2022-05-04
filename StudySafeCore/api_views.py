# from curses import reset_prog_mode
# from modulefinder import ReplacePackage
# # from selectors import EpollSelector
# from sre_constants import SUCCESS

from django.http import Http404
# from itsdangerous import Serializer
from itertools import chain
from django.conf import settings

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
    queryset = Venue.objects.all()
    serializer_class = VenueSerialization

class MemberViewSet(viewsets.ModelViewSet):
    queryset = HKUMember.objects.all()
    serializer_class = HKUMemberSerialization

class VenueEntryExitRecordViewSet(viewsets.ModelViewSet):
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = VenueEntryExitRecordSerialization

class ExitRecordView(generics.GenericAPIView):
    
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = ExitRecordSerialization

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
        
        serializer = ExitRecordSerialization(instance,data=request.data,partial=True)
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
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetVisitedVenuesView(generics.GenericAPIView):
    
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = GetVisitedVenuesSerialization

    def get(self, request,*args, **kwargs):

        request_serializer = GetVisitedVenuesSerialization(data=request.GET)
        if request_serializer.is_valid():
            dateDiagnosis = datetime(request_serializer.validated_data["dateDiagnosis"].year, request_serializer.validated_data["dateDiagnosis"].month, request_serializer.validated_data["dateDiagnosis"].day,23,59,59);
            queryResult = VenueEntryExitRecord.objects.filter(
                hkuMember=HKUMember.objects.get(HKUID=request_serializer.validated_data["hkuMember"]),
                entryDatetime__range=[
                   dateDiagnosis - timedelta(days=3) + timedelta(minutes=1), dateDiagnosis]).exclude(duration=None)
            
            #use list->dict->list to remove duplicates
            visitedVenuesCode = list(set([i.venue.venueCode for i in queryResult]))
            visitedVenuesCode.sort()
            
            response = {}
            response["visited venues"] = []
            for v in visitedVenuesCode:
                venue_serializer = VenueSerialization(Venue.objects.get(venueCode = v))
                response["visited venues"].append(venue_serializer.data)
            
            return Response(response,status=status.HTTP_200_OK)
            
        else:
            return Response(request_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetCloseContactsView(generics.GenericAPIView):
    
    queryset = VenueEntryExitRecord.objects.all()
    serializer_class = GetCloseContactsSerialization

    def get(self, request,*args, **kwargs):

        request_serializer = GetVisitedVenuesSerialization(data=request.GET)
        if request_serializer.is_valid():
            
            dateDiagnosis = datetime(request_serializer.validated_data["dateDiagnosis"].year, request_serializer.validated_data["dateDiagnosis"].month, request_serializer.validated_data["dateDiagnosis"].day,23,59,59);
            patient_visit_records = VenueEntryExitRecord.objects.filter(
            hkuMember=HKUMember.objects.get(HKUID=request_serializer.validated_data["hkuMember"]),duration__gte=timedelta(minutes=30),
            entryDatetime__range=[dateDiagnosis - timedelta(days=3) + timedelta(minutes=1), dateDiagnosis])

            closeContactsUID = set()
            for r in patient_visit_records:
                #cat 1, contact enters before patient enters, contact exit after patient enters but before patient exit
                contactExitTime = r.entryDatetime + timedelta(minutes=30)
                close_contacts_1 = VenueEntryExitRecord.objects.filter(venue=r.venue,
                entryDatetime__lte=r.entryDatetime,
                exitDatetime__lte=r.exitDatetime,
                exitDatetime__gte=contactExitTime).exclude(duration=None)
                #cat 2, contacts enters after patient enters, contact exit before patient exit
                close_contacts_2 = VenueEntryExitRecord.objects.filter(venue=r.venue,
                entryDatetime__gte=r.entryDatetime,
                exitDatetime__lte=r.exitDatetime,
                duration__gte=timedelta(minutes=30)).exclude(duration=None)
                #cat 3, contacts enters before patient exit, contact exit after patient exit
                contactEntryTime = r.exitDatetime - timedelta(minutes=30)
                close_contacts_3 = VenueEntryExitRecord.objects.filter(venue=r.venue,
                exitDatetime__gte=r.exitDatetime,
                entryDatetime__gte=r.entryDatetime,
                entryDatetime__lte=contactEntryTime).exclude(duration=None)
                #cat 4, contacts enters before patient enters, contact exit after patient exit
                close_contacts_4 = VenueEntryExitRecord.objects.filter(venue=r.venue,
                entryDatetime__lte=r.entryDatetime,
                exitDatetime__gte=r.exitDatetime,
                duration__gte=timedelta(minutes=30)).exclude(duration=None)
                
                # print(f'1: {close_contacts_1}')
                # print(f'2: {close_contacts_2}')
                # print(f'3: {close_contacts_3}')
                # print(f'4: {close_contacts_4}')

                close_contacts = close_contacts_1 | close_contacts_2 |close_contacts_3 |close_contacts_4
                for cR in close_contacts:
                    closeContactsUID.add(cR.hkuMember.HKUID)
            if request_serializer.validated_data["hkuMember"] in closeContactsUID:
                closeContactsUID.remove(request_serializer.validated_data["hkuMember"])
            closeContactsUID = list(closeContactsUID)
            closeContactsUID.sort()
            response = {}
            response["close contacts"] = []
            for c in closeContactsUID:
                hkuMember_serializer = HKUMemberSerialization(HKUMember.objects.get(HKUID = c))
                response["close contacts"].append(hkuMember_serializer.data)
        
            return Response(response,status=status.HTTP_200_OK)
            
        else:
            return Response(request_serializer.errors,status=status.HTTP_400_BAD_REQUEST)