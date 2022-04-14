from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.

class BaseView(TemplateView):
    template_name = 'base.html'

class VenuesView(TemplateView):
    template_name = 'venues.html'

class ContactsView(TemplateView):
    template_name = 'contacts.html'