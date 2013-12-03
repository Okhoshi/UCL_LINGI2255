# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout
from django.contrib.auth.models import User as DUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext_lazy as _
from forms import MForm
from exceptions import *
from website.models import *

# Non logged decorator
def login_forbidden(function=None, redirect_field_name=None, redirect_to='account'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def home(request):
    testimonies = Testimony.get_random_testimonies(3, request.LANGUAGE_CODE)
    return render(request, 'home.html', {'testimonies': testimonies})

@login_forbidden
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

def concept(request):
    return render(request, 'concept.html', {})

def contact(request):
    return render(request, 'contact.html', {})



def register(request):
    return render(request, 'register.html', {})


def individual_registration(request):
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            print(request.FILES.items())
            handle_uploaded_file(request.FILES['file'])
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
            return redirect('account')
        else:
            error = True
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            dictionaries['errorlist'] = form.errorlist
            return render(request, 'individual_registration.html', dictionaries)

    return render(request, 'individual_registration.html', {})


def handle_uploaded_file(f):
    with open('media/profilepics/t', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def organisation_registration(request):
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            p = Place(country=form.country, postcode=form.postcode,
                      city=form.city, street=form.street,
                      number=form.streetnumber)
            p.save()
            assoc = Association(location=p, name=form.org_name, description=form.description)
            assoc.save()
            user = AssociationUser.objects.create_user(form.user_name,
                                                       form.email,
                                                       form.passwd,
                                                       assoc, 0,
                                                       first_name=form.first_name,
                                                       last_name=form.name)

            usr = authenticate(username=form.user_name, password=form.passwd)
            Dlogin(request, usr)
            return redirect('account')
        else:
            error = True
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            dictionaries['errorlist'] = form.errorlist
            return render(request, 'organisation_registration.html', dictionaries)

    return render(request, 'organisation_registration.html', {})

@login_required
def account(request):
    return render(request, 'account.html', {})

@login_required
def profile(request):
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)
    current_offers = []
    current_demands = []
    old_requests = []
    feedbacks = []
    rating = 0
    entity = None
    if (is_user):
        entity = is_user[0]

    elif (is_association_user):
        au = is_association_user[0]
        entity = au.entity

    if (entity):
        current_offers = entity.get_current_offers()
        current_demands = entity.get_current_demands()
        old_requests = entity.get_old_requests()
        feedbacks = entity.get_feedback()
        rating = entity.get_rating()

    current_offers_demander_list = []
    for elem in current_offers:
        demand = elem.demander
        name_demand = ""
        demand_assoc = Association.objects.filter(entity_ptr_id__exact=demand.id)
        demand_user = User.objects.filter(entity_ptr_id__exact=demand.id)


        if (demand_assoc):
            demand = demand_assoc[0]
            name_demand = demand.name
        elif (demand_user): #is a User
            demand = demand_user[0]
            demand = DUser.objects.get(id=demand.dj_user_id)
            name_demand = demand.first_name + " " + demand.last_name
        current_offers_demander_list.append((elem, name_demand, elem.date))
    current_offers = current_offers_demander_list


    current_demands_proposer_list = []
    for elem in current_demands:
        proposer = elem.proposer
        name_proposer = ""

        proposer_assoc = Association.objects.filter(entity_ptr_id__exact=proposer.id)
        proposer_user = User.objects.filter(entity_ptr_id__exact=proposer.id)
        if (proposer_assoc):
            proposer = proposer_assoc[0]
            name_proposer = proposer.name
        elif (proposer_user): #is a User
            proposer = proposer_user[0]
            proposer = DUser.objects.get(id=proposer.dj_user_id)
            name_proposer = proposer.first_name + " " + proposer.last_name
        current_demands_proposer_list.append((elem, name_proposer, elem.date))
    current_demands = current_demands_proposer_list



    return render(request, 'profile.html', {'entity': entity, \
        'current_offers':current_offers, 'current_demands':current_demands, \
        'old_requests':old_requests, 'feedbacks':feedbacks , 'rating':rating})

@login_required
def create_offer_demand(request):
    return render(request, 'create.html', {})

@login_required
def add_representative(request):
    return render(request, 'add_representative.html', {})

@login_required
def logout(request):
    Dlogout(request)
    return redirect('home')
