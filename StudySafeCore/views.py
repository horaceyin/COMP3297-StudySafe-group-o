from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# for testing
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.

def Testing(request):
    return HttpResponse(os.path.join(BASE_DIR) + '/tesing')