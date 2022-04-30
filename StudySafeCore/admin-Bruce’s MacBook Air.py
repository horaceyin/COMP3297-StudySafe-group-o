from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(HKUMember)
admin.site.register(Venue)
admin.site.register(VenueEntryExitRecord)