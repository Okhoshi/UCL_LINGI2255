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
from django.utils.translation import ugettext as _

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
    print(request)
    if request.method == 'POST':
        #form = MForm(request)
        #if form.is_valid:
            print(request.FILES.items())
            #handle_uploaded_file(request.FILES['file'])
            #p = Place(country=form.country, postcode=form.postcode,\
            #          city=form.city, street=form.street,\
            #         number=form.streetnumber)
            #p.save()
            #user = User.objects.create_user(form.user_name,\
            #                               form.email,\
            #                                form.passwd,\
            #                                first_name=form.first_name,\
            #                                last_name=form.name,\
            #                                location=p)
            # Log on the newly created user
            #usr = authenticate(username=form.user_name, password=form.passwd)
            #Dlogin(request, usr)
            #return redirect('account')
        #else:
            #error = True
            #dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            #dictionaries['errorlist'] = form.errorlist
            #return render(request, 'contact.html', {})

            #return render(request, 'contact.html', dictionaries)

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
    is_verified = None
    current_offers = []
    current_demands = []
    old_requests = []
    feedbacks = []
    rating = 0;
    global_rating = 0
    tuple_rating = None
    entity = None
    image = None
    if (is_user):
        entity = is_user[0]
        image = entity.picture
        is_verified = entity.is_verified
    elif (is_association_user):
        au = is_association_user[0]
        entity = au.entity
        image = entity.picture
        is_verified = 1

    if (entity):
        current_offers = entity.get_current_offers()
        current_demands = entity.get_current_demands()
        old_requests = entity.get_old_requests()
        feedbacks = entity.get_feedback()
        tuple_rating = entity.get_rating()
        value_rating = 100.0 * float(tuple_rating[2]+tuple_rating[0]) / float(sum(tuple_rating))
        global_rating = (value_rating,sum(tuple_rating))
    current_offers_demander_list = []
    for elem in current_offers:
        demand = elem.demander
        name_demand = "/"
        demand_assoc = []
        demand_user = []
        if (demand):
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
        proposer_assoc = []
        proposer_user = []
        if (proposer):
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


    history = []
    for elem in old_requests:
        other = None
        type_req = ""
        if (elem.demander.id == entity.id):
            other = elem.proposer
            type_req = _('demanded')
        elif (elem.proposer.id == entity.id):
            other = elem.demander
            type_req = _('proposed')

        name_other = "/"

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if (other_assoc):
            other = other_assoc[0]
            name_other = other.name
        elif (other_user): #is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name
        history.append((elem, type_req, name_other, elem.date))
    old_requests = history

    rating_values = ["danger","","success"]
    feedbacks_list = []
    for elem in feedbacks[0]:
        other = None
        req = elem.request

        feedback = elem.feedback_proposer
        rating = elem.rating_proposer
        other = elem.request.proposer

        name_other = ""

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if (other_assoc):
            other = other_assoc[0]
            name_other = other.name
        elif (other_user): #is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name

        feedbacks_list.append(((elem.request, name_other, feedback), rating_values[rating-1]))
        
    for elem in feedbacks[1]:
        other = None
        req = elem.request

        feedback = elem.feedback_demander
        rating = elem.rating_demander
        other = elem.request.demander

        name_other = ""

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if (other_assoc):
            other = other_assoc[0]
            name_other = other.name
        elif (other_user): #is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name
        feedbacks_list.append(((elem.request, name_other, feedback), rating_values[rating-1]))





    feedbacks = feedbacks_list
    return render(request, 'profile.html', {'entity': entity, \
        'current_offers':current_offers, 'current_demands':current_demands, \
        'old_requests':old_requests, 'feedbacks':feedbacks , 'global_rating':global_rating, \
        'image':image, 'is_verified':is_verified})

@login_required
def create_offer_demand(request):
    return render(request, 'create.html', {})

@login_required
def add_representative(request):
    if request.method == 'POST':
        last_name = request.POST.getlist('last_name[]')
        first_name = request.POST.getlist('first_name[]')
        email = request.POST.getlist('email[]')
        level = request.POST.getlist('memberLevel[]')

        for i in range(len(last_name)):
            print('We add ',last_name[i],first_name[i],email[i],level[i])
            # TODOOOOO - Je ferai ca ce soir ou demain matin apres avoir lu la doc :) 
    
    return render(request, 'add_representative.html', {})

@login_required
def logout(request):
    Dlogout(request)
    return redirect('home')
