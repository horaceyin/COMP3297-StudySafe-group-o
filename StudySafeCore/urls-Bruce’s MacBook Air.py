from StudySafeCore import views
from . import services
#the above is useless

from django.urls import path, include
from .api_views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'venues/<str:pk>', VenueViewSet, 'venue')
router.register(r'venues', VenueViewSet, 'venue')
router.register(r'hku-members', MemberViewSet)
router.register(r'entry-exit-records', VenueEntryExitRecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

# urlpatterns = [
#     # path('api/venues/create', services.VenuesCreate),
#     # path('api/venues/list-all', list_all_venues.as_view(), name='all_venues'),
#     # path('api/contacts/', services.Contacts),
#     # # above for testing
#     # path('api/members/all', services.MembersListAll),
# ]
