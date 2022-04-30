import email
from django.db import models

# Create your models here.
class HKUMember(models.Model):
  HKUID = models.CharField(max_length=10, primary_key=True)
  name = models.CharField(max_length=150)
  def __str__(self):
    return f'ID: {self.HKUID}, Name: {self.name}'

class Venue(models.Model):
  venueCode = models.CharField(max_length=20, primary_key=True)
  location = models.CharField(max_length=150)
  type = models.CharField(max_length=3)
  capacity = models.IntegerField()
  # hkuMember = models.ManyToManyField(HKUMember, through='VenueEntryExitRecord')
  def __str__(self):
    return f'{self.location} ({self.venueCode}) type: {self.type} capacity: {self.capacity}'

class VenueEntryExitRecord(models.Model):
  entryDatetime = models.DateTimeField()
  exitDatetime = models.DateTimeField(blank=True, null=True)
  duration = models.DurationField(blank=True, null=True)
  venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
  hkuMember = models.ForeignKey(HKUMember, on_delete=models.CASCADE)
  def __str__(self):
    return f'{self.hkuMember.HKUID} {self.venue.venueCode} ({self.entryDatetime})'

# class TaskForceMember(models.Model):
#   username = models.CharField(max_length=100, primary_key=True)
#   password = models.CharField(max_length=100, primary_key=True)
#   firstname = models.CharField(max_length=100, primary_key=True)
#   lastname = models.CharField(max_length=100, primary_key=True)
#   email = models.CharField(max_length=100, primary_key=True)

#   def __str__(self):
#     return f'Username: {self.username}, Password: {self.password}, First Name: {self.firstname}, Last Name: {self.lastname}, Email:{self.email}'