from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {})

def individual_registration(request):
    return render(request, 'individual_registration.html', {})

def organisation_registration(request):
    return render(request, 'organisation_registration.html', {})
