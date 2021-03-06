# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.templatetags.static import static
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User as DUser
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime as dt
from forms import MForm,RForm,SolidareForm, PForm, CForm, FeedbackForm
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
    # Testimonies
    testimonies = Testimony.get_random_testimonies(3, request.LANGUAGE_CODE)

    # Latest requests
    latest_requests = FilteredRequest.get_latest_requests(amount=6)

    latest_requests_tuples = []
    for req in latest_requests:
        latest_requests_tuples.append((req, \
            profile_current_demands([req])[0][1],\
            profile_current_offers([req])[0][1], \
            profile_current_offers([req])[0][2]))

    return render(request, 'home.html', {'testimonies': testimonies,
                                         'latest_requests':latest_requests_tuples})


def news(request):
    return render(request, 'news.html', {})


@login_forbidden
def login(request):
    message = None
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


def faq(request):
    return render(request, 'faq.html', {})


def contact(request):
    if request.method == 'POST':
        form = CForm(request)
        if form.is_valid:
            user = settings.EMAIL_HOST_USER
            pwd = settings.EMAIL_HOST_PASSWORD

            data = request.POST.dict()
            user = settings.EMAIL_HOST_USER
            admin = ['quentin.deconinck@student.uclouvain.be', 'romain.vanwelde@student.uclouvain.be',
                 'q.devos@student.uclouvain.be', 'martin.crochelet@student.uclouvain.be',
                 'benjamin.baugnies@student.uclouvain.be', 'jordan.demeulenaere@student.uclouvain.be']
            obj = "Solidare-It Contact "
            message = "Comment or request from " + data.get('title') + ". "+ data.get('name') + " " +\
                      data.get('first_name') + "\n \n"
            message += "Address of the user : " + data.get('street') + ", " + data.get('streetnumber') + " " +\
                        data.get('postcode') + " " + data.get('city') + " " + data.get('country') + "\n"
            message += "Email of the user : " + data.get('email') + "\n \n"
            message += "Comments  : \n" + data.get('comments')


            send_mail(obj, message, user, admin, fail_silently=False)


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
    type = request.GET.get('type', False)

    if request.method == 'GET':
        pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
        return render(request, pages.get(type, 'register.html'), {})

    elif request.method == 'POST':
        if request.GET.get('type', False):
            return analyse_request(request, type)
        else:
            return render(request, 'register.html', {})
    else:
        return render(request, 'register.html', {})

@login_required
def edit_profile(request):
    """ handle the registration of a user
    """
    type = request.GET.get('type', False)
    usr = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=usr.id).count()
    is_association_user = AssociationUser.objects.filter(dj_user__exact=usr.id).count()
    my_child = None
    if is_user:
        type = "1"
        my_child = User.objects.get(dj_user=usr.id)
    elif is_association_user:
        type = "2"
        my_child = AssociationUser.objects.get(dj_user=usr.id)
    else:
        type = "0"

    edit = True

    if request.method == 'GET':
        pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
        if is_user:
            return render(request, pages.get(type, 'register.html'), {'name':usr.last_name, \
                                                                      'first_name':usr.first_name, \
                                                                      'birthdate':my_child.birth_day.strftime("%Y-%m-%d"), \
                                                                      'gender':my_child.gender, \
                                                                      'user_name':usr.username, \
                                                                      'email':usr.email, \
                                                                      'street':my_child.location.street, \
                                                                      'streetnumber':my_child.location.number, \
                                                                      'city':my_child.location.city, \
                                                                      'postcode':my_child.location.postcode, \
                                                                      'country':my_child.location.country, \
                                                                      'profile_pic':my_child.picture, \
                                                                      'id_card':my_child.id_card,
                                                                      'edit': edit})
        if is_association_user:
            assoc = my_child.entity
            return render(request, pages.get(type, 'register.html'), {'name':usr.last_name, \
                                                                      'first_name':usr.first_name, \
                                                                      'birthdate':my_child.birth_day.strftime("%Y-%m-%d"), \
                                                                      'gender':my_child.gender, \
                                                                      'user_name':usr.username, \
                                                                      'email':usr.email, \
                                                                      'street':assoc.location.street, \
                                                                      'streetnumber':assoc.location.number, \
                                                                      'city':assoc.location.city, \
                                                                      'postcode':assoc.location.postcode, \
                                                                      'country':assoc.location.country, \
                                                                      'profile_pic':my_child.picture, \
                                                                      'description':assoc.description,\
                                                                      'org_name':assoc.name, \
                                                                      'org_pic':assoc.picture,
                                                                      'edit':edit})

    elif request.method == 'POST':
        return analyse_request_edit(request, type, usr)
    else:
        return render(request, 'register.html', {})


@login_required
def add_representative(request):
    # This page can only be reached by association users
    this_user = DUser.objects.get(username=request.user)
    is_association_user = AssociationUser.objects.filter(dj_user=this_user.id)
    if not is_association_user:
        return redirect('account')
    else:
        au = is_association_user[0]

    if request.method == 'POST':
        form = RForm(request)
        if form.is_valid:
            success_messages = []
            for row in form.rows:
                ###########################################
                ##### Store the AssociationUser in DB #####
                ###########################################

                password = DUser.objects.make_random_password()
                email = row['email']
                username = email.split('@')[0]
                last_name = row['last_name']
                first_name = row['first_name']
                level = int(row['level'])
                assoc = au.get_association()
                birthdate = datetime.datetime.utcnow().replace(tzinfo=utc)

                index = 2
                base_username = username
                while DUser.objects.filter(username = username).count() != 0:
                    username = "%s%s" % (base_username,index)
                    index += 1

                auser = AssociationUser.objects.create_user(
                    username = username,
                    password = password,
                    email = email,
                    level = level,
                    association = assoc,
                    last_name = last_name,
                    first_name = first_name,
                    birth_day = birthdate)

                #######################################
                ##### Success message on the page #####
                #######################################
                
                if level == 0:
                    level_str = _("administrator")
                else:
                    level_str = _("member")
                message = first_name + " " + last_name + _(" has successfully been added as ")\
                    + level_str + "."
                success_messages.append(message)


                #########################
                ##### Send the mail #####
                #########################

                user = settings.EMAIL_HOST_USER
                dest = [email]
                obj = "Solidare-It - Added to " + assoc.name
                message = _("Dear ") + first_name + " " + last_name + ",\n\n"
                message += _("This mail is sent to warn you that an account related to the association ") + \
                    assoc.name + _(" has been created for you on Solidare-It.\n")
                message += _("You can log in at http://") + get_current_site(request).domain + _("/login/ with the username and password that have been generated especially for you :\n\n")
                message += _("Username : ") + username + "\n"
                message += _("Password : ") + password + "\n\n"
                message += _("You possess the status of ") + level_str + ".\n\n"
                message += _("The Solidare-It Team.")

                send_mail(obj, message, user, dest, fail_silently=False)

            return render(request, 'add_representative.html',
                    {'rows':[{}],'success_messages':success_messages})
        else:
            rows = form.rows if form.rows else [{}]
            return render(request, 'add_representative.html', \
                {'errorlist':form.errorlist,\
                 'rows':rows})

    return render(request, 'add_representative.html', {'rows':[{}]})


@login_required
def add_pins(request):
    # This page can only be reached by association users
    this_user = DUser.objects.get(username=request.user)
    is_association_user = AssociationUser.objects.get(dj_user=this_user.id)
    if not is_association_user:
        return redirect('account')
    else:
        au = is_association_user
        list_users = {}
        for org_usr in  au.get_association().get_employees():
            list_users[org_usr.dj_user.get_full_name()] = org_usr

    if request.method == 'POST':
        form = PForm(request)
        if form.is_valid:
            success_messages = []
            for row in form.rows:
                ###########################################
                ##### Store the PIN in DB #####
                ###########################################

                last_name = row['last_name']
                first_name = row['first_name']
                managed_by = list_users.get(row['managed_by'])

                new_pin = PIN(first_name=first_name, last_name=last_name, managed_by=managed_by)
                new_pin.save()

                message = first_name + " " + last_name + _(" has successfully been added and managed by ")\
                    + managed_by.dj_user.get_full_name() + "."
                success_messages.append(message)


                #########################
                ##### Send the mail #####
                #########################

                user = settings.EMAIL_HOST_USER
                dest = [managed_by.dj_user.email]
                obj = "Solidare-It - Added to " + managed_by.get_association().name
                message = _("Dear ") + managed_by.dj_user.first_name + " " + managed_by.dj_user.last_name + ",\n\n"
                message += _("This mail is sent to warn you that a PIN related to the association ") + \
                    managed_by.get_association().name + _(" has been created on Solidare-It.\n")
                message += _("Your new PIN client is ") + first_name + " " + last_name + "\n\n"
                message += _("The Solidare-It Team.")

                send_mail(obj, message, user, dest, fail_silently=False)

            return render(request, 'add_pins.html',
                    { 'rows' : [{}], 'success_messages':success_messages, 'list_users':list_users})
        else:
            rows = form.rows if form.rows else [{}]
            return render(request, 'add_pins.html', {'errorlist':form.errorlist,'rows':rows, 'list_users':list_users})

    return render(request, 'add_pins.html', {'rows':[{}], 'list_users':list_users})


@login_required
def account(request):
    if request.method == 'POST':
        suppress = request.POST.get('suppress')
        if not suppress == None:            
            to_suppress = SavedSearch.objects.get(id=suppress)
            to_suppress.delete()
        feedback = request.POST.get('feedback')
        if not feedback == None:
            form = FeedbackForm(request)
            feedback_to_fill = Feedback.objects.get(id = form.feedback_id)
            if  form.is_proposer == '1':
                feedback_to_fill.rating_proposer = form.rating
                feedback_to_fill.feedback_proposer = form.feedback
            else :                
                feedback_to_fill.rating_demander = form.rating
                feedback_to_fill.feedback_demander = form.feedback
            feedback_to_fill.save()

        

    req_id = request.REQUEST.get('req_id')
    candid_id = request.REQUEST.get('candid_id')


    finish_req = request.REQUEST.get('finish_req')


    susp_req_id = request.REQUEST.get('susp_req_id')
    if susp_req_id :
        req_to_mod = Request.objects.get(id=susp_req_id)
        req_to_mod.is_suspicious = True
        req_to_mod.save()
        return redirect('account')


    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)

    saved_searches = []
    similar = []
    pending = []
    following = []
    image = None
    upcoming_requests = []
    summary = (0,0,0)
    type_user = 0

    is_association_admin = False
    is_association = False
    ## GET CURRENT ENTITY AND PICTURE
    if (is_user):
        entity = is_user[0]
        image = entity.picture
        type_user = 1

        #is_verified = entity.is_verified
    elif (is_association_user):
        au = is_association_user[0]
        entity = au.entity
        image = entity.picture
        type_user = 2
        is_association = True
        if au.level == 0:
            is_association_admin = True

        #is_verified = 1

    empty_feedback = []
    if (is_user or is_association_user):

        #TREATS GET REQUESTS WITH USER VERIFICATION
        if finish_req:
            finish_req = Request.objects.get(id=finish_req)
            if entity.id == finish_req.demander.id or entity.id == finish_req.proposer.id :
                if not finish_req.state==Request.DONE:
                    finish_req.state = Request.DONE
                    finish_req.save()
                    new_feedback = Feedback()
                    new_feedback.request = finish_req
                    new_feedback.save()

        if req_id and candid_id:
            request_to_change = Request.objects.get(id=req_id)
            if True or (not request_to_change.demander == None and entity.id == request_to_change.demander.id) or (not request_to_change.proposer == None and entity.id == request_to_change.proposer.id) :
                candid_obj = Entity.objects.get(id=candid_id)
                print(sol_user(candid_obj))
                b = request_to_change.candidates.all()
                if (candid_obj in b) and (not candid_obj == entity):
                    if request_to_change.proposer:
                        request_to_change.demander = candid_obj
                    else:
                        request_to_change.proposer = candid_obj
                    request_to_change.state = Request.IN_PROGRESS
                    request_to_change.candidates = []
                    request_to_change.save()

        
        ##GET UN-GIVEN FEEDBACK
        needed_feedback = entity.get_feedback()
        for feedback in needed_feedback[0]:
            if feedback.rating_demander == 0:
                f_request = feedback.request
                f_proposer = sol_user(f_request.proposer)
                f_demander = sol_user(f_request.demander)
                f_req_cat = f_request.category
                f_subject = f_request.name
                f_place = f_request.place
                f_date = f_request.date
                f_values = {'proposer' : f_proposer,
                               'demander' : f_demander,
                               'request_category' : f_req_cat,
                               'request_subject' : f_subject,
                               'request_place' : f_place,
                               "request_date" : f_date,
                                'is_proposer': 0,
                                'feed_ID': feedback.id}
                empty_feedback.append((feedback, f_values))
        for feedback in needed_feedback[1]:
            if feedback.rating_proposer == 0:
                f_request = feedback.request
                f_proposer = sol_user(f_request.proposer)
                f_demander = sol_user(f_request.demander)
                f_req_cat = f_request.category
                f_subject = f_request.name
                f_place = f_request.place
                f_date = f_request.date
                f_values = {'proposer' : f_proposer,
                               'demander' : f_demander,
                               'request_category' : f_req_cat,
                               'request_subject' : f_subject,
                                'request_place' : f_place,
                               "request_date" : f_date,
                                'is_proposer': 1,
                                'feed_ID': feedback.id}
                empty_feedback.append((feedback, f_values))
    
            
        
        
        ## GET FOLLOWING LIST
        for person in entity.get_followed():
            following.append((person, sol_user(person).__unicode__()))

        ## GET SAVED SEARCHES
        objects_saved_searches = entity.get_searches()
        for elem in objects_saved_searches:
            saved_searches.append((elem, elem.search_field))

        ## GET SIMILAR
        similar_objects = entity.get_similar_matching_requests(6)
        i = 0
        for elem in similar_objects:
            if i < 3:
                a = (elem, profile_current_demands([elem])[0][1], profile_current_offers([elem])[0][1], elem.name)
                if search_filter_can_be_added(elem, entity, is_user):
                    similar.append(a)
                    i += 1

        ## GET Pending
        
        pending_objects = entity.get_all_requests().filter(state__exact=Request.PROPOSAL)
        for elem in pending_objects:
            req_candidates = []
            req_candidates_obj = list(elem.candidates.all().exclude(id__exact=entity.id))
            if req_candidates_obj:
                for candid in req_candidates_obj:      
                    req_candidates.append(sol_user(candid))            
                a = (elem, profile_current_demands([elem])[0][1], profile_current_offers([elem])[0][1], req_candidates)
                pending.append(a)                   
    
        ## GET UPCOMING REQUESTS
        upcoming_requests = []
        upcoming_objects = entity.get_current_requests()
        for elem in upcoming_objects:
            a = (elem, profile_current_demands([elem])[0][1], profile_current_offers([elem])[0][1], elem.name)
            upcoming_requests.append(a)   


        ## GET # OLD REQUEST
        old_requests = entity.get_old_requests().count()
        in_progress_requests = upcoming_objects.count()
        proposal_requests = entity.get_current_offers().count() + \
            entity.get_current_demands().count() - in_progress_requests
        summary = (proposal_requests, in_progress_requests, old_requests)
        
    return render(request, 'account.html', {'image': image, 'following': following,
                                            'saved_searches': saved_searches, 'similar': similar,
                                            'upcoming_requests': upcoming_requests, 'summary': summary,
                                            'is_association_admin': is_association_admin,
                                            'type_user': type_user, 'pending': pending,
                                            'empty_feedback':empty_feedback,
                                            'is_association':is_association})


@login_required
def profile(request):

    # First, check if the current user is a User or a AssociationUser
    this_user = DUser.objects.get(username=request.user)
    this_entity = None
    this_entity = None

    is_user = User.objects.filter(dj_user__exact=this_user)
    if is_user:
        is_user = is_user[0]
        this_entity = is_user

    is_association = AssociationUser.objects.filter(dj_user__exact=this_user)
    if is_association:
        is_association = is_association[0].get_association()
        this_entity = is_association

    my_profile = True

    entity = None
    follow = None

    profile_id = request.REQUEST.get('profile_id')
    if profile_id:
        user_visited = User.objects.filter(entity_ptr__exact=profile_id)

        if user_visited:
            user_visited = user_visited[0]
            entity = user_visited

        association_visited = Association.objects.filter(entity_ptr__exact=profile_id)
        if association_visited:
            association_visited = association_visited[0]
            entity = association_visited

        if entity == this_entity:
            my_profile = True
        else:
            my_profile = False

        if entity and this_entity and not my_profile:
            follow = False
            for elem in this_entity.get_followed():
                if elem.id == entity.id:
                    follow = True


            if request.method == 'POST':
                if 'follow_ask' in request.POST:
                    this_entity.set_followed(entity)
                    follow = True

                elif 'unfollow_ask' in request.POST:
                    this_entity.remove_followed(entity)
                    follow = False
        this_entity = entity
        is_user = user_visited

    is_verified = None
    if is_user:
        is_verified = is_user.confirmed_status

    image = this_entity.picture
    profile_name = this_entity.__unicode__()

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
        total_rating = sum(tuple_rating)
        if total_rating != 0:
            value_rating = 100.0 * float(tuple_rating[2] + tuple_rating[0]) / float(sum(tuple_rating))
        else:
            value_rating = 0
        global_rating = (value_rating, sum(tuple_rating))

    # Then format the data for the template
    current_offers_tuples=[]
    current_demands_tuples = []
    old_tuples = []
    feedback_tuples = []

    for req in current_offers:
        current_offers_tuples.append((req, profile_current_demands([req])[0][1], profile_current_offers([req])[0][1], profile_current_offers([req])[0][2]))
    for req in current_demands:
        current_demands_tuples.append((req, profile_current_demands([req])[0][1], profile_current_offers([req])[0][1], profile_current_demands([req])[0][2]))
    old_requests = profile_old_requests(old_requests, this_entity)
    
    for elem in old_requests:
        old_tuples.append((elem[0], profile_current_demands([elem[0]])[0][1], profile_current_offers([elem[0]])[0][1], elem[1], elem[2], elem[3]))
    if feedbacks:
        feedbacks = profile_feedbacks(feedbacks)
        for feed in feedbacks:
            if feed[0][2]:
                feedback_tuples.append((feed[0][0], feed[1], profile_current_offers([feed[0][0]])[0][1], feed[0][1], feed[0][2], feed[0][3]))
    # Finally return all the useful informations
    return render(request, 'profile.html', {'entity': this_entity,
                                            'current_offers': current_offers_tuples,
                                            'current_demands': current_demands_tuples,
                                            'old_requests': old_tuples, 'feedbacks': feedback_tuples,
                                            'global_rating': global_rating, 'profile_name':profile_name,
                                            'image': image, 'is_verified': is_verified, 'my_profile':my_profile,
                                            'profile_id': profile_id, 'follow': follow})


@login_required
def create_offer_demand(request):
    DEF_MIN_RATING = 2
    dictionnary = {}
    usr = DUser.objects.get(username=request.user)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=usr.id).count()
    if request.method == 'POST':
        form = SolidareForm(request)
        dictionnary = form.values
        if form.is_valid:
            # Getting the place
            if form.values['country'] or form.values['postcode'] or\
                form.values['city'] or form.values['street'] or\
                form.values['streetnumber']:
                place = Place(country = form.values['country'] if form.values['country'] != '' else None, \
                    postcode = form.values['postcode'] if form.values['postcode'] != '' else None,\
                    city = form.values['city'] if form.values['city'] != '' else None, \
                    street = form.values['street'] if form.values['street'] != '' else None,\
                    number = form.values['streetnumber'] if form.values['streetnumber'] != '' else None)
                place.save()
            else:
                place = Place()
                place.save()

            # Getting the date
            date = None
            if form.values['date']:
                date = form.values['date']

            # Getting the user
            this_user = DUser.objects.get(username = request.user)
            is_user = User.objects.filter(dj_user__exact = this_user.id)
            is_association_user = AssociationUser.objects.filter(dj_user__exact = this_user.id)
            entity = None
            if is_user:
                entity = is_user[0]
            elif is_association_user:
                au = is_association_user[0]
                entity = au.entity

            # Setting as demander or proposer
            proposer = None
            demander = None
            pin_proposer = None
            pin_demander = None

            if form.values['type'] == 'offer':
                proposer = entity
                if not form.values['pin_selected'] == "None":
                    pin_proposer = form.values['pin_selected']
                    pin_proposer = PIN.objects.get(id=pin_proposer)
            elif form.values['type'] == 'demand':
                demander = entity
                if not form.values['pin_selected'] == "None":
                    pin_demander = form.values['pin_selected']
                    pin_demander = PIN.objects.get(id=pin_demander)
    

            req = None
            # Filtered Request
            if form.values['filters'] == 'on':
                only_verified = True if form.values['verified'] == 'on' \
                            else False
                min_rating = DEF_MIN_RATING if form.values['min_rating'] == 'on'\
                            else None
                gender = form.values['gender']
                min_age = int(form.values['min_age']) if form.values['min_age'] != ''\
                    else None
                max_age = int(form.values['max_age']) if form.values['max_age'] != ''\
                    else None

                req = FilteredRequest(name = form.values['description'],
                    date = date,
                    category = form.values['category'],
                    place = place,
                    proposer = proposer,
                    demander = demander,
                    pin_proposer = pin_proposer,
                    pin_demander = pin_demander,
                    state = Request.PROPOSAL)
                req.only_verified = only_verified
                req.min_rating = min_rating
                req.gender = gender
                req.save()

                age_filter = AgeFilter(min_age = min_age,
                    max_age = max_age,
                    filtered_request = req)
                age_filter.save()

            # Non-filtered request
            else:
                req = Request(name = form.values['description'],
                    date = date,
                    category = form.values['category'],
                    place = place,
                    proposer = proposer,
                    demander = demander,
                    pin_demander = pin_demander,
                    pin_proposer = pin_proposer,
                    state = Request.PROPOSAL)
                req.save()

            return redirect('account')

        else:
            dictionnary['errorlist'] = form.errorlist
            for key,value in form.colors.items():
                dictionnary[key] = value
    dictionnary['au'] = is_association_user
    if is_association_user:
        association_user = AssociationUser.objects.get(dj_user=usr.id)
        dictionnary['pin'] = association_user.get_pin()
    return render(request, 'create.html', dictionnary)


@login_required
def logout(request):
    Dlogout(request)
    return redirect('home')


@login_required
def messages(request):

    def qs_add(qs, item):
        if qs and item:
            qs.add(item)
        return qs

    usr = DUser.objects.get(username=request.user)

    if User.is_user(usr.id):
        entity = User.objects.get(dj_user=usr.id)
    elif AssociationUser.is_assoc_user(usr.id):
        entity = AssociationUser.objects.get(dj_user=usr.id).entity
    else:
        return redirect('home')

    messages = None
    req_id = None
    possible_rec = []

    if request.method == "POST":
        if request.POST.get('type') and request.POST.get('id'):
            req_id = request.POST.get('id')
            req = Request.objects.get(id=req_id)

            if request.POST['type'] == "1" and request.POST.get('receiver')\
               and request.POST.get('message-content', '') != '':


                mess = InternalMessage(time=dt.now(utc),
                                       sender=entity, request=Request.objects.get(id=req_id),
                                       message=request.POST.get('message-content'),
                                       receiver=Entity.objects.get(id=request.POST.get('receiver')))
                mess.save()
                return HttpResponse("")

            elif request.POST['type'] == "2":
                # Associate the current user with the request
                req.candidates.add(entity)
                req.save()
                return HttpResponse("")

                #Force Open the modal
            elif request.POST['type'] == "3":
                messages = InternalMessage.objects.filter(request_id__exact=req_id).order_by('time')
                messages = map(lambda m: (sol_user(m.sender), sol_user(m.receiver), m.message, m.time, m.sender.id == entity.id or m.receiver.id == entity.id), messages)
                possible_rec = map(lambda r: sol_user(r), qs_add(qs_add(req.candidates, req.proposer), req.demander).exclude(id__exact=entity.id))
                return render(request, 'message_display.html', {'request_id': req_id, 'messages': messages, 'possible_receivers' : possible_rec})

    if request.method == "GET":
        req_id = request.GET.get('id')

    threads = entity.get_all_requests(include_candidates=True).exclude(state__exact=Request.DONE).order_by('-date')
    threads = map(lambda t: (t.id, t.name, sol_user(InternalMessage.objects.filter(request_id__exact=t.id).order_by('-time')[0].sender).picture if InternalMessage.objects.filter(request_id__exact=t.id).count() != 0 else None, ", ".join(map(lambda m: sol_user(m).__unicode__(), qs_add(qs_add(t.candidates, t.proposer), t.demander).exclude(id__exact=entity.id)))), threads)

    if req_id:
        found = False
        for th in threads:
            if long(req_id) == th[0]:
                found = True
                break
        if not found:
            req_id = None

    return render(request, 'messages.html', {'threads': threads, 'request_id': req_id})


##
## Display list of exchanges of the user
##
@login_required
def exchanges(request):   

    # First, check if the current user is a User or a AssociationUser
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)
    this_entity = None
    if is_user:
        this_entity = is_user[0]
    elif is_association_user:
        au = is_association_user[0]
        this_entity = au.entity

    # Then, fetch some useful data from the models
    posted_req = []
    candidate_req = []
    incoming_req = []
    realised_req = []
    feedback_req = []

    percentage_req = []

    # Should always pass, except if user is a superuser
    if this_entity:
        all_req = this_entity.get_all_requests()
        for elem in all_req:

            # List of PROPOSAL requests with candidates
            if (elem.state == Request.PROPOSAL) and elem.candidates.all().exclude(id__exact=this_entity.id):
                demander = profile_current_offers( [elem] )[0][1]
                offer = profile_current_demands([elem])[0][1]
                candidate_req.append((elem,offer,demander))

            # List of PROPOSAL requests witout candidates
            if (elem.state == Request.PROPOSAL) and not elem.candidates.all().exclude(id__exact=this_entity.id):
                demander = profile_current_offers( [elem] )[0][1]
                offer = profile_current_demands([elem])[0][1]
                posted_req.append((elem,offer,demander))

            # List of IN_PROGRESS requests
            if elem.state == Request.IN_PROGRESS:
                demander = profile_current_offers([elem])[0][1]
                offer = profile_current_demands([elem])[0][1]
                incoming_req.append((elem,offer,demander))

            # List of DONE requests
            if elem.state == Request.DONE:
                if elem.demander.id == this_entity.id:
                    has_a_feedback =  elem.get_feedback().rating_demander > 0
                else:
                    has_a_feedback =  elem.get_feedback().rating_proposer > 0

                # With Feedbacks already given
                if has_a_feedback:
                    demander = profile_current_offers([elem])[0][1]
                    offer = profile_current_demands([elem])[0][1]
                    feedback_req.append((elem,offer,demander))

                # Without Feedbacks
                else:
                    demander = profile_current_offers([elem])[0][1]
                    offer = profile_current_demands([elem])[0][1]
                    realised_req.append((elem,offer,demander))


        # create tuple with percentage of each request's type
        sum_req = (len(posted_req),len(candidate_req),\
            len(incoming_req),len(realised_req),len(feedback_req))
        total = sum(sum_req)
        if total == 0:
            percentage_req = (0,0,0,0,0)
        else:
            for elem in sum_req:
               percentage_req.append((elem * 100) / total)

    return render(request, 'exchanges.html', {'posted_req':posted_req, \
        'candidate_req':candidate_req, 'incoming_req':incoming_req, \
        'realised_req':realised_req,'feedback_req':feedback_req,\
        'percentage_req':percentage_req})


@login_required()
def search(request):
    search_results = []
    usr = DUser.objects.get(username=request.user)
    is_user = 0

    if User.is_user(usr.id):
        usr_entity = User.objects.get(dj_user=usr.id)
        is_user = 1
    elif AssociationUser.is_assoc_user(usr.id):
        usr_entity = AssociationUser.objects.get(dj_user=usr.id).entity
    else:
        return redirect('login')
    searched = False
    max_times = 0
    if request.method == 'POST':
        search_field = request.POST['search']

        if 'search_saved' in request.POST.dict():
            if search_field == "" :
                return render(request, 'search.html', {'search_results':search_results,
                                                   'max_times':max_times, 'search_saved_invalid':'INVALID'})
            else :
                pla = Place()
                pla.save()
                savedsearch = SavedSearch(place=pla, search_field=search_field, entity=usr_entity)
                savedsearch.save()
                return render(request, 'search.html', {'search_saved': "True", 'search_results':search_results,
                                                   'max_times':max_times, 'searched':searched})

        else:
            search_object = SavedSearch(search_field=search_field)
            search_objects = usr_entity.search(search_object, 30)
            searched = True
            i = 0
            for this_request in search_objects:
                if i < 15:
                    (req_initiator, req_type) = this_request.get_initiator()
                    # Need to know if it's a User or a Association
                    initiator_entity = sol_user(req_initiator)
                    if search_filter_can_be_added(this_request, usr_entity, is_user): # Verify if it pass the filters
                        search_results.append((this_request, req_type, initiator_entity, this_request.place, this_request.date))
                        i += 1
            max_times = len(search_results)
            return render(request, 'search.html', {'search_field': search_field, 'search_results':search_results,
                                                   'max_times':max_times, 'searched':searched})
    if request.method == 'GET':
        search_field = request.GET.get('id')
        if search_field:
            search_object = SavedSearch(search_field=search_field)
            search_objects = usr_entity.search(search_object, 20)
            searched = True
            i = 0
            for this_request in search_objects:
                if i < 15:
                    (req_initiator, req_type) = this_request.get_initiator()
                    # Need to know if it's a User or a Association
                    initiator_entity = sol_user(req_initiator)
                    if search_filter_can_be_added(this_request, usr_entity, is_user): # Verify if it pass the filters
                        search_results.append((this_request, req_type, initiator_entity, this_request.place, this_request.date))
                        i += 1
            max_times = len(search_results)
            return render(request, 'search.html', {'search_field': search_field, 'search_results':search_results,
                                                   'max_times':max_times, 'searched':searched})

    return render(request, 'search.html', {'search_results':search_results, 'max_times':max_times, 'searched':searched})




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
        name_demand = None
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
            is_offer = (False)
            other_is_demander = False
        elif elem.proposer.id == this_entity.id:
            other = elem.demander
            is_offer = (True)
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

        history.append((elem, is_offer, name_other, elem.date))

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
        is_offer = False

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

        feedbacks_list.append(((elem.request, name_other, feedback, is_offer), rating_values[rating - 1]))

    # Then check the feedback of its offers
    for elem in feedbacks[1]:
        feedback = elem.feedback_demander
        rating = elem.rating_demander
        other = elem.request.demander
        is_offer = True

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
        feedbacks_list.append(((elem.request, name_other, feedback, is_offer), rating_values[rating - 1]))

    return feedbacks_list


def sol_user(entity):
    if User.objects.filter(entity_ptr__exact=entity).count() != 0:
        return User.objects.get(entity_ptr=entity)
    elif Association.objects.filter(entity_ptr__exact=entity).count() != 0:
        return Association.objects.get(entity_ptr=entity)
    else:
        return entity


def analyse_request_edit(request, type, usr):
    form = MForm(request, usr=usr)
    pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
    if form.is_valid:
        if type == "1":
            # individual code
            return modify_user(request, form)
        elif type == "2":
            # organisation code
            return modify_organisation(request, form)
        else:
            return render(request, 'register.html', request.POST)
    else:
        error = True
        dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
        dictionaries['errorlist'] = form.errorlist
        return render(request, pages[type], dictionaries)


def analyse_request(request, type):
    form = MForm(request)
    pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
    if form.is_valid:
        if type == "1":
            # individual code
            return create_new_user(request, form)
        elif type == "2":
            # organisation code
            return create_new_organisation(request, form)
        else:
            return render(request, 'register.html', request.POST)
    else:
        error = True
        dictionaries = dict(form.colors.items() + request.POST.dict().items() + locals().items())
        dictionaries['errorlist'] = form.errorlist
        return render(request, pages[type], dictionaries)


def modify_user(request, form):
    p = Place(country=form.country, postcode=form.postcode,
              city=form.city, street=form.street,
              number=form.streetnumber)
    p.save()

    # Django User
    dusr = DUser.objects.get(username=request.user)
    dusr.username = form.user_name
    dusr.email = form.email
    dusr.set_password(form.passwd)
    dusr.first_name = form.first_name
    dusr.last_name = form.name

    # User
    usr = User.objects.get(dj_user=dusr)
    usr.location = p
    usr.birth_day = form.birthdate
    usr.gender = form.gender
    if request.FILES.get('profile_pic') is not None:
        usr.picture.save(request.FILES.get('profile_pic').name,
                          request.FILES.get('profile_pic'),
                          save=False)
    if request.FILES.get('id_card_pic') is not None:
        usr.id_card.save(request.FILES.get('id_card_pic').name,
                          request.FILES.get('id_card_pic'),
                          save=False)

    # Database
    dusr.save()
    usr.save()
    # Log on the newly created user
    Dlogout(request)
    newusr = authenticate(username=form.user_name, password=form.passwd)
    Dlogin(request, newusr)
    return redirect('account')


def modify_organisation(request, form):
    p = Place(country=form.country, postcode=form.postcode,
              city=form.city, street=form.street,
              number=form.streetnumber)
    p.save()

    # Django User modify
    dusr = DUser.objects.get(username=request.user)
    dusr.username = form.user_name
    dusr.email = form.email
    dusr.set_password(form.passwd)
    dusr.first_name = form.first_name
    dusr.last_name = form.name


    # AssociationUser modify
    ausr = AssociationUser.objects.get(dj_user=dusr)
    ausr.gender = form.gender
    ausr.birth_day = form.birthdate
    # Don't change the level or the association!!!
    if request.FILES.get('profile_pic') is not None:
        ausr.picture.save(request.FILES.get('profile_pic').name,
                          request.FILES.get('profile_pic'),
                          save=False)

    # Association modify
    assoc = ausr.entity
    assoc.location = p
    assoc.name = form.org_name
    assoc.description = form.description
    if request.FILES.get('org_pic') is not None:
        assoc.picture.save(request.FILES.get('org_pic').name,
                          request.FILES.get('org_pic'),
                          save=False)


    # Save all in DB
    dusr.save()
    assoc.save()
    ausr.entity = assoc
    ausr.save()

    # Relog in
    Dlogout(request)
    usr = authenticate(username=form.user_name, password=form.passwd)
    Dlogin(request, usr)

    return redirect('account')


def create_new_user(request, form):

    p = Place(country=form.country, postcode=form.postcode,
              city=form.city, street=form.street,
              number=form.streetnumber)
    p.save()
    user = User.objects.create_user(form.user_name,
                                    form.email,
                                    form.passwd,
                                    first_name=form.first_name,
                                    last_name=form.name,
                                    location=p, birth_day=form.birthdate, gender=form.gender)
    if request.FILES.get('profile_pic') is not None:
        user.picture.save(request.FILES.get('profile_pic').name,
                          request.FILES.get('profile_pic'),
                          save=False)
    if request.FILES.get('id_card_pic') is not None:
        user.id_card.save(request.FILES.get('id_card_pic').name,
                          request.FILES.get('id_card_pic'),
                          save=False)
    user.save()
    # Log on the newly created user
    usr = authenticate(username=form.user_name, password=form.passwd)
    Dlogin(request, usr)
    return redirect('account')


def create_new_organisation(request, form):

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
                                               last_name=form.name,
                                               birth_day=form.birthdate,
                                               gender=form.gender)
    user.dj_user.is_active = False
    user.dj_user.save()

    if request.FILES.get('profile_pic') is not None:
        user.picture.save(request.FILES.get('profile_pic').name,
                          request.FILES.get('profile_pic'),
                          save=False)
    if request.FILES.get('org_pic') is not None:
        assoc.picture.save(request.FILES.get('org_pic').name,
                          request.FILES.get('org_pic'),
                          save=False)
    assoc.save()
    user.save()
    #usr = authenticate(username=form.user_name, password=form.passwd)
    #Dlogin(request, usr)


    return redirect('account')


def handle_uploaded_file(f, filename, path):
    if f is not None:
        with open(path+'_'+filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


def search_filter_can_be_added(this_request, usr_entity, is_user):
    """
    Function that indicates if this_request can be broadcast to usr_entity
    @param this_request: the request to know
    @param usr_entity: the entity to know
    @return: True is this_request can be shown to usr_entity, False otherwise
    """
    if not is_user:
        # Don't try to manage with the Association: there are assumed to be verified
        return True
    if not FilteredRequest.objects.filter(request_ptr=this_request).count(): # If this_request is not a FilteredRequest
        return True
    freq = FilteredRequest.objects.get(request_ptr=this_request)
    # First check the verified status
    if freq.only_verified:
        if not usr_entity.confirmed_status:
            return False
    # Then check the gender
    if not freq.gender == User.UNSPECIFIED:
        if not freq.gender == usr_entity.gender:
            return False
    # Now based on the rating
    # Ok if at least 50% of satisfaction
    if freq.min_rating:
        rating = usr_entity.get_rating()
        if sum(rating) == 0 or float(rating[1])/sum(rating) > 0.5:
            return False
    # Eventually, the Age Filters
    age_filters = freq.get_age_filter()
    if not age_filters:
        # No filters, so ok
        return True
    age_usr = usr_entity.get_age()
    for afilter in age_filters:
        in_filter = True
        if afilter.min_age:
            if age_usr <= afilter.min_age:
                in_filter = False
        if in_filter and afilter.max_age:
            if age_usr >= afilter.max_age:
                in_filter = False
        if in_filter:
            return True
    # No in the filters, so don't show it
    return False
