# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import HKUMember
# from .serializers import MembersSerializer
# # API for StudySafe Core

# def VenuesCreate():
#     pass

# def VenuesListAll():
#     pass

# def Contacts():
#     pass

# @api_view(['GET'])
# def MembersListAll(request):
#     allMembers = HKUMember.objects.all()
#     allMembers_serializer = MembersSerializer(allMembers, many = True)
#     return Response(allMembers_serializer.data)