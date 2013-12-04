# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout
from django.contrib.auth.models import User as DUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext_lazy as _
from forms import MForm,RForm
from exceptions import *
from website.models import *
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

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
        form = MForm(request)
        if form.is_valid:
            user = settings.EMAIL_HOST_USER
            pwd = settings.EMAIL_HOST_PASSWORD
            admin = ['quentin.deconinck@student.uclouvain.be', 'romain.vanwelde@student.uclouvain.be',
                     'q.devos@student.uclouvain.be', 'martin.crochelet@student.uclouvain.be',
                     'benjamin.baugnies@student.uclouvain.be', 'jordan.demeulenaere@student.uclouvain.be']
            data = request.POST.dict()
            message = "Comment or request from " + data.get('title') + ". "+ data.get('name') + " " +\
                      data.get('first_name') + "\n \n"
            message += "Address of the user : " + data.get('street') + ", " + data.get('streetnumber') + " " +\
                        data.get('postcode') + " " + data.get('city') + " " + data.get('country') + "\n"
            message += "Email of the user : " + data.get('email') + "\n \n"
            message += "Comments  : \n" + data.get('comments')

            print(message)

            send_mail('Solidare-It Contact', message, user, admin, fail_silently=False)

            return render(request, 'contact.html', {'request_done': True})
        else:
            error = True
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            dictionaries['errorlist'] = form.errorlist

            return render(request, 'contact.html', dictionaries)

    return render(request, 'contact.html', {})

@login_forbidden()
def register(request):
    """ handle the registration of a user
    """
    if request.method == 'GET':
        type = request.GET.get('type', False)
        if type:
            if type == "1":
                return render(request, 'individual_registration.html', {})
            elif type == "2":
                return render(request, 'organisation_registration.html', {})
            else:
                return render(request, 'register.html', {})
        else:
            return render(request, 'register.html', {})
    elif request.method =='POST':
        type = request.GET.get('type', False)
        if type:
            return analyse_request(request, type)
        else:
            return render(request, 'register.html', {})
    else:
        return render(request, 'register.html', {})

def analyse_request(request, type):
    form = MForm(request)
    pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            print("do something !")
            return render(request, pages[type], request.POST)
        else:
            error = True
            dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
            dictionaries['errorlist'] = form.errorlist
            return render(request, pages[type], dictionaries)

@login_required
def add_representative(request):
        # for i in range(len(last_name)):
        #     print('We add ', last_name[i], first_name[i], email[i], level[i])
        # TODOOOOO - Je ferai ca ce soir ou demain matin apres avoir lu la doc :)

    return render(request, 'add_representative.html', {})


def individual_registration(request):
    if request.method == 'POST':
        form = MForm(request)
        if form.is_valid:
            print(request.FILES.items())
            handle_uploaded_file(request.FILES['file'])
            p = Place(country=form.country, postcode=form.postcode, \
                      city=form.city, street=form.street, \
                      number=form.streetnumber)
            p.save()
            user = User.objects.create_user(form.user_name, \
                                            form.email, \
                                            form.passwd, \
                                            first_name=form.first_name, \
                                            last_name=form.name, \
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
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)


    saved_searches = []
    similar = []
    following = []
    image = None
    upcoming_requests = []
    summary = []

    ## GET CURRENT ENTITY AND PICTURE
    if (is_user):
        entity = is_user[0]
        image = entity.picture
        #is_verified = entity.is_verified
    elif (is_association_user):
        au = is_association_user[0]
        entity = au.entity
        image = entity.picture
        #is_verified = 1

    if (is_user or is_association_user):
        ## GET FOLLOWING LIST
        following_entity = entity.get_followed()
        for person in following_entity:
            person_assoc = Association.objects.filter(entity_ptr_id__exact=person.id)
            person_user = User.objects.filter(entity_ptr_id__exact=person.id)

            if (person_assoc):
                person = person_assoc[0]
                name_person = person.name
            elif (person_user): #is a User
                person = person_user[0]
                person = DUser.objects.get(id=person.dj_user_id)
                name_person = person.first_name + " " + person.last_name
            following.append(name_person)

        ## GET SAVED SEARCHES
        objects_saved_searches = entity.get_searches()
        for elem in objects_saved_searches:
            saved_searches.append((elem, elem.search_field))

        ## GET SIMILAR
        similar_objects = entity.get_similar_matching_requests(3)
        for elem in similar_objects:
            similar.append((elem,elem.name))

        ## GET UPCOMING REQUESTS
        upcoming_requests = []
        upcoming_objects = entity.get_current_requests()
        for elem in upcoming_objects:
            upcoming_requests.append((elem,elem.date))
    


        ## GET # OLD REQUEST
        old_requests = entity.get_old_requests().count()
        in_progress_requests = upcoming_objects.count()
        proposal_requests = entity.get_current_offers().count() + \
            entity.get_current_demands().count() - in_progress_requests
        summary = (proposal_requests,in_progress_requests,old_requests)

    return render(request, 'account.html', {'image':image,'following':following,\
        'saved_searches':saved_searches,'similar':similar,\
        'upcoming_requests':upcoming_requests,'summary':summary})


@login_required
def profile(request):
    # First, check if the current user is a User or a AssociationUser
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)
    is_verified = None
    this_entity = None
    image = None
    if is_user:
        this_entity = is_user[0]
        image = this_entity.picture
        is_verified = this_entity.is_verified
    elif is_association_user:
        au = is_association_user[0]
        this_entity = au.entity
        image = this_entity.picture
        is_verified = 1 # A active association must be verified

    # Then, fetch some useful data from the models
    current_offers = []
    current_demands = []
    old_requests = []
    feedbacks = []
    global_rating = 0
    tuple_rating = None

    # Should always pass, except if user is a superuser
    if this_entity:
        current_offers = this_entity.get_current_offers()
        current_demands = this_entity.get_current_demands()
        old_requests = this_entity.get_old_requests()
        feedbacks = this_entity.get_feedback()
        tuple_rating = this_entity.get_rating()
        value_rating = 100.0 * float(tuple_rating[2] + tuple_rating[0]) / float(sum(tuple_rating))
        global_rating = (value_rating, sum(tuple_rating))

    # Then format the data for the template
    current_offers = profile_current_offers(current_offers)
    current_demands = profile_current_demands(current_demands)
    old_requests = profile_old_requests(old_requests, this_entity)
    if feedbacks:
        feedbacks = profile_feedbacks(feedbacks)

    # Finally return all the useful informations
    return render(request, 'profile.html', {'entity': entity, \
                                            'current_offers': current_offers, 'current_demands': current_demands, \
                                            'old_requests': old_requests, 'feedbacks': feedbacks,
                                            'global_rating': global_rating, \
                                            'image': image, 'is_verified': is_verified})


@login_required
def create_offer_demand(request):
    return render(request, 'create.html', {})


@login_required
def logout(request):
    Dlogout(request)
    return redirect('home')

@login_required
def messages(request):
    return render(request, 'messages.html', {'messages': list(range(18))})


###############################################################################
########################SUBROUTINES IMPLEMENTED HERE###########################
###############################################################################
def profile_current_offers(current_offers):
    """
    Method that format the current_offers from the models for the template
    @param current_offers: the current_offers from the models
    @return: well formatted current offers for the template profile
    """
    current_offers_demander_list = []
    for elem in current_offers:
        demand = elem.demander
        name_demand = "/"
        demand_assoc = []
        demand_user = []
        # Check if a demander is found or not; if it's the case, determine if a
        # Association or a User
        if demand:
            demand_assoc = Association.objects.filter(entity_ptr_id__exact=demand.id)
            demand_user = User.objects.filter(entity_ptr_id__exact=demand.id)

        # Check if it's a User or a Association
        if demand_assoc: # is a Association
            demand = demand_assoc[0]
            name_demand = demand.name
            # If a PIN is defined
            if elem.pin_demander:
                name_demand += ' (' + elem.pin_demander.first_name + ' ' + \
                               elem.pin_demander.last_name + ')'
        elif demand_user: # is a User
            demand = demand_user[0]
            demand = DUser.objects.get(id=demand.dj_user_id)
            name_demand = demand.first_name + " " + demand.last_name

        current_offers_demander_list.append((elem, name_demand, elem.date))

    return current_offers_demander_list


def profile_current_demands(current_demands):
    """
    Method that format the current_demands from the models for the template
    @param current_demands: the current_demands from the models
    @return: well formatted current demands for the template profile
    """
    current_demands_proposer_list = []
    for elem in current_demands:
        proposer = elem.proposer
        name_proposer = ""
        proposer_assoc = []
        proposer_user = []
        # Check if a proposer is found or not; if it's the case, determine if a
        # Association or a User
        if proposer:
            proposer_assoc = Association.objects.filter(entity_ptr_id__exact=proposer.id)
            proposer_user = User.objects.filter(entity_ptr_id__exact=proposer.id)
            # Check if it's a User or a Association
        if proposer_assoc: # is a Association
            proposer = proposer_assoc[0]
            name_proposer = proposer.name
            # If a PIN is defined
            if elem.pin_proposer:
                name_proposer += ' (' + elem.pin_proposer.first_name + ' ' + \
                                 elem.pin_proposer.last_name + ')'
        elif proposer_user: #is a User
            proposer = proposer_user[0]
            proposer = DUser.objects.get(id=proposer.dj_user_id)
            name_proposer = proposer.first_name + " " + proposer.last_name

        current_demands_proposer_list.append((elem, name_proposer, elem.date))

    return current_demands_proposer_list


def profile_old_requests(old_requests, this_entity):
    """
    Method that format the history from the models for the template
    @param old_requests: the old_requests from the models
    @return: well formatted history for the template profile
    """
    history = []
    for elem in old_requests:
        other = None
        type_req = ""
        other_is_demander = False
        if elem.demander.id == this_entity.id:
            other = elem.proposer
            type_req = _('demanded')
            other_is_demander = False
        elif elem.proposer.id == this_entity.id:
            other = elem.demander
            type_req = _('proposed')
            other_is_demander = True

        name_other = "/"

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if other_assoc: # is a Association
            other = other_assoc[0]
            name_other = other.name
            if other_is_demander:
                if elem.pin_demander:
                    name_other += ' (' + elem.pin_demander.first_name + ' ' + \
                                  elem.pin_demander.last_name + ')'
            else:
                if elem.pin_proposer:
                    name_other += ' (' + elem.pin_proposer.first_name + ' ' + \
                                  elem.pin_proposer.last_name + ')'
        elif other_user: # is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name

        history.append((elem, type_req, name_other, elem.date))

    return history


def profile_feedbacks(feedbacks):
    """
    Method that format the feedback from the models for the template
    @param get_feedbacks: the get_feedbacks from the models
    @return: well formatted feedbacks for the template profile
    """
    # Class name for the template row
    rating_values = ["danger", "", "success"]

    feedbacks_list = []
    # First check the feedback of its demands
    for elem in feedbacks[0]:
        # The proposer gives its feedback about the request
        feedback = elem.feedback_proposer
        rating = elem.rating_proposer
        other = elem.request.proposer

        name_other = ""

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if other_assoc: # is a Association
            other = other_assoc[0]
            name_other = other.name
            if elem.request.pin_proposer:
                    name_other += ' (' + elem.request.pin_proposer.first_name + ' ' + \
                                  elem.request.pin_proposer.last_name + ')'
        elif other_user: #is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name

        feedbacks_list.append(((elem.request, name_other, feedback), rating_values[rating - 1]))

    # Then check the feedback of its offers
    for elem in feedbacks[1]:
        feedback = elem.feedback_demander
        rating = elem.rating_demander
        other = elem.request.demander

        name_other = ""

        other_assoc = Association.objects.filter(entity_ptr_id__exact=other.id)
        other_user = User.objects.filter(entity_ptr_id__exact=other.id)

        if other_assoc: # is a Association
            other = other_assoc[0]
            name_other = other.name
            if elem.request.pin_demander:
                    name_other += ' (' + elem.request.pin_demander.first_name + ' ' + \
                                  elem.request.pin_demander.last_name + ')'
        elif other_user: #is a User
            other = other_user[0]
            other = DUser.objects.get(id=other.dj_user_id)
            name_other = other.first_name + " " + other.last_name
        feedbacks_list.append(((elem.request, name_other, feedback), rating_values[rating - 1]))

    return feedbacks_list
