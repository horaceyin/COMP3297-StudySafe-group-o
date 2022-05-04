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
    path('api/exit/',ExitRecordView.as_view()),
    path('api/entry/',EntryRecordView.as_view()),
    path('api/visitedVenues/',GetVisitedVenuesView.as_view()),
    path('api/closeContacts/',GetCloseContactsView.as_view())
]