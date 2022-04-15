from django.urls import path, include
from StudySafeCore import views
from . import services
from .api_views import VenueViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'venues/<str:pk>', VenueViewSet, 'venue')
router.register(r'venues', VenueViewSet, 'venue')

urlpatterns = [
    # path('api/venues/create', services.VenuesCreate),
    # path('api/venues/list-all', list_all_venues.as_view(), name='all_venues'),
    path('api/', include(router.urls)),
    # path('api/contacts/', services.Contacts),
    # # above for testing
    # path('api/members/all', services.MembersListAll),
]