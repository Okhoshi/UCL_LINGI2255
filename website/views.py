# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as Dlogin
from django.contrib.auth.decorators import login_required
from models import *

def home(request):
    testimonies = Testimony.get_random_testimonies(3)
    return render(request, 'home.html', {'testimonies': testimonies})

def login(request):
    message = request
    if request.POST.__contains__('username'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                Dlogin(request, user)
                # Redirect to a success page.
                if request.REQUEST.__contains__('next'):
                    return redirect(request.REQUEST['next'], permanent=False)
                else:
                    return redirect('profile', permanent=False)
            else:
                # Return a 'disabled account' error message
                message = 'Disabled Account'
        else:
            # Return an 'invalid login' error message.
            message = 'Invalid login'
    return render(request, 'login.html', {'message': message, 'redirect': request.REQUEST.get('next','')})

def register(request):
    return render(request, 'register.html', {})

def individual_registration(request):
    return render(request, 'individual_registration.html', {})

def organisation_registration(request):
    return render(request, 'organisation_registration.html', {})

@login_required
def profile(request):
    return render(request, 'profile.html', {})

def add_representative(request):
    return render(request, 'add_representative.html', {})