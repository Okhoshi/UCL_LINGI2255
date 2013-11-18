# Create your views here.
from django.shortcuts import render
from models import *

def home(request):
    testimonies = Testimony.get_random_testimonies(3)
    return render(request, 'home.html', {'testimonies': testimonies})

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {})

def individual_registration(request):
    return render(request, 'individual_registration.html', {})

def organisation_registration(request):
    return render(request, 'organisation_registration.html', {})

def profile(request):
    return render(request, 'profile.html', {})