# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
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
                    return redirect('account')
            else:
                # Return a 'disabled account' error message
                message = _("This account has been disabled. " + \
                            "Please contact the administrator of this site.")
        else:
            # Return an 'invalid login' error message.
            message = _("This username or password is not valid.")
    return render(request, 'login.html', \
                  {'message': message, 'redirect': request.REQUEST.get('next', '')})


def register(request):
    return render(request, 'register.html', {})


def individual_registration(request):
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            p = Place(country=form.country, postcode=form.postcode,\
                      city=form.city, street=form.street,\
                      number=form.streetnumber)
            p.save()
            user = User.objects.create_user(form.user_name,\
                                            form.email,\
                                            form.passwd,\
                                            first_name=form.first_name,\
                                            last_name=form.name,\
                                            location=p)
            # Log on the newly created user
            usr = authenticate(username=form.user_name, password=form.passwd)
            Dlogin(request, usr)
            return redirect('home')
        else:
            error = True
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            dictionaries['errorlist'] = form.errorlist
            return render(request, 'individual_registration.html', dictionaries)

    return render(request, 'individual_registration.html', {})


def organisation_registration(request):
    return render(request, 'organisation_registration.html', {})

@login_required
def account(request):
    return render(request, 'account.html', {})

@login_required
def profile(request):
    return render(request, 'profile.html', {})


@login_required
def add_representative(request):
    return render(request, 'add_representative.html', {})


def logout(request):
    Dlogout(request)
    return redirect('home')
