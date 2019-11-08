#from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Anchor

def index(request):
    return render(request, 'home.html')
    #return HttpResponse("Anchors Generator for Human Vaccine Project")
