# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout#, \
    #user as DUser
from django.contrib.auth.decorators import login_required
from forms import MForm
from exceptions import *
from website.models import *


def home(request):
    testimonies = Testimony.get_random_testimonies(3)
    return render(request, 'home.html', {'testimonies': testimonies})


def login(request):
    message = request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                Dlogin(request, user)
                # Redirect to a success page.
                if request.REQUEST.__contains__('next'):
                    return redirect(request.REQUEST['next'])
                else:
                    return redirect('profile')
            else:
                # Return a 'disabled account' error message
                message = 'Disabled Account'
        else:
            # Return an 'invalid login' error message.
            message = 'Invalid login'
    return render(request, 'login.html', \
                  {'message': message, 'redirect': request.REQUEST.get('next', '')})


def register(request):
    return render(request, 'register.html', {})


def individual_registration(request):
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            p = Place(country=request.POST.get('country'), postcode=request.POST.get('postcode'),\
                      city=request.POST.get('city'), street=request.POST.get('street'),\
                      number=request.POST.get('streetnumber'))
            p.save()
            user = User.objects.create_user(request.POST['user_name'],\
                                            request.POST['email'],\
                                            request.POST['passwd'],\
                                            first_name=request.POST.get('first_name'),\
                                            last_name=request.POST.get('name'),\
                                            location=p)
            return redirect('home')
        else:
            error = True;
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items()+['errorlist', form.errorlist])
            print(dictionaries)
            return render(request, 'individual_registration.html', dictionaries)

    return render(request, 'individual_registration.html', {})


def organisation_registration(request):
    return render(request, 'organisation_registration.html', {})


@login_required
def profile(request):
    return render(request, 'profile.html', {})


@login_required
def add_representative(request):
    return render(request, 'add_representative.html', {})


def logout(request):
    Dlogout(request)
    return redirect('home')
