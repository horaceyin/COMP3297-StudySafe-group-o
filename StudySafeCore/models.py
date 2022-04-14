# from django.db import models

# # Create your models here.
# class HKUMember(models.Model):
#   HKUID = models.CharField(max_length=10, primary_key=True)
#   name = models.CharField(max_length=150)
#   def __str__(self):
#     return f'ID: {self.HKUID}, Name: {self.name}'

# class Venue(models.Model):
#   venueCode = models.CharField(max_length=20, primary_key=True)
#   location = models.CharField(max_length=150)
#   type = models.CharField(max_length=3)
#   capacity = models.IntegerField()
#   hkuMember = models.ManyToManyField(HKUMember, through='VenueEntryExitRecord')
#   def __str__(self):
#     return f'{self.location} ({self.venueCode}) type: {self.type} capacity: {self.capacity}'

# class VenueEntryExitRecord(models.Model):
#   entryOrExit = models.BooleanField()
#   recordDatetime = models.DateTimeField()
#   venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
#   hkuMember = models.ForeignKey(HKUMember, on_delete=models.CASCADE)
#   def __str__(self):
#     return f'{self.hkuMember.HKUID} {self.venue.venueCode} ({self.recordDatetime})'