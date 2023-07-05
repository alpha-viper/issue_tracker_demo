from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


import datetime

def home(request):
    
    print('Home function is called from view')
    return HttpResponse("Page 1")
