# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, \
    login as Dlogin, \
    logout as Dlogout
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User as DUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext_lazy as _
from forms import MForm,RForm,SolidareForm
from exceptions import *
from website.models import *
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from datetime import datetime
from django.templatetags.static import static

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

def news(request):
    return render(request, 'news.html', {})

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


def faq(request):
    return render(request, 'faq.html', {})


def contact(request):
    if request.method == 'POST':
        # FOR FEEDBACK
        if 'feedback' in request.POST.dict():
            # As a request is in the state "Done", a feedback has been created
            # feedback = request.get_feedback()
            #data = request.POST.dict()

            #if request.proposer == user :
            #    feedback.feedback_proposer = data.get('feedback')
            #    feedback.rating_proposer = data.get('rating')
            #else
            #    feedback.feedback_demander = data.get('feedback')
            #    feedback.rating_demander = data.get('rating')
            print('coucou')

            return render(request, 'contact.html', {})

        else:
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

    # For feedback
    proposer = "Moi"
    demander = "Toi"
    request_category = "Chaussettes"
    request_subject = "Echanges"
    request_place = "Bxl"
    request_date = "Ajd"
    feedback_values = {'proposer' : proposer,
                       'demander' : demander,
                       'request_category' : request_category,
                       'request_subject' : request_subject,
                       'request_place' : request_place,
                       "request_date" : request_date}

    return render(request, 'contact.html', feedback_values)


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

    if request.method == 'GET':
        usr = DUser.objects.get(username=request.user)
        is_user = User.objects.filter(dj_user__exact=usr.id).count()
        is_association_user = AssociationUser.objects.filter(dj_user__exact=usr.id).count
        my_child = None
        if is_user:
            type = "1"
            my_child = User.objects.get(dj_user=usr.id)
        elif is_association_user:
            type = "2"
            my_child = AssociationUser.objects.get(dj_user=usr.id)
        else:
            type = "0"
        pages = {"1": 'individual_registration.html', "2": 'organisation_registration.html'}
        return render(request, pages.get(type, 'register.html'), {'name':usr.last_name, 'first_name':usr.first_name, 'birthdate':my_child.birth_day, 'gender':my_child.gender, 'user_name':usr.username, 'email':usr.email, 'street':my_child.location.street})

    elif request.method == 'POST':
        if request.GET.get('type', False):
            return analyse_request(request, type)
        else:
            return render(request, 'register.html', {})
    else:
        return render(request, 'register.html', {})


@login_required
def add_representative(request):
    # This page can only be reached by association users
    this_user = DUser.objects.get(username=request.user)
    is_association_user = AssociationUser.objects.get(dj_user=this_user.id)
    if not is_association_user:
        return redirect('account')
    else:
        au = is_association_user

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

                index = 2
                while DUser.objects.filter(username = username).count() != 0:
                    username = "%s%s" % (username,index)
                    index += 1

                auser = AssociationUser.objects.create_user(
                    username = username,
                    password = password,
                    email = email,
                    level = level,
                    association = assoc,
                    last_name = last_name,
                    first_name = first_name)

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
def account(request):
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)
    
    saved_searches = []
    similar = []
    following = []
    image = None
    upcoming_requests = []
    summary = (0,0,0)
    type_user = 0

    is_association_admin = False
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
        if au.level == 0:
            is_association_admin = True

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
            a=(elem, profile_current_offers([elem])[0][1], profile_current_demands([elem])[0][1], elem.name)
            similar.append(a)
            print('##########' , a)
                
    
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
        'upcoming_requests':upcoming_requests,'summary':summary,\
        'is_association_admin': is_association_admin,\
        'type_user':type_user})


@login_required
def profile(request):

    # First, check if the current user is a User or a AssociationUser
    this_user = DUser.objects.get(username=request.user)
    is_user = User.objects.filter(dj_user__exact=this_user.id)
    is_association_user = AssociationUser.objects.filter(dj_user__exact=this_user.id)
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        is_user = User.objects.filter(entity_ptr_id__exact=profile_id)
        is_association_user = AssociationUser.objects.filter(entity_id=profile_id)
       
    is_verified = None
    this_entity = None
    image = None
    #print(is_user)
    if is_user:
        this_entity = is_user[0]
        image = this_entity.picture
        is_verified = this_entity.is_verified
        this_entity_name = DUser.objects.get(id=this_entity.dj_user_id)
        profile_name = this_entity_name.first_name + " " + this_entity_name.last_name
    elif is_association_user:
        au = is_association_user[0]
        this_entity = au.entity
        image = this_entity.picture
        is_verified = 1
        profile_name = this_entity.name 

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
        print(feedbacks)

    # Finally return all the useful informations
    return render(request, 'profile.html', {'entity': entity, \
                                            'current_offers': current_offers_tuples, 'current_demands': current_demands_tuples, \
                                            'old_requests': old_tuples, 'feedbacks': feedbacks, \
                                            'global_rating': global_rating, 'profile_name':profile_name, \
                                            'image': image, 'is_verified': is_verified})


@login_required
def create_offer_demand(request):
    DEF_MIN_RATING = 2
    dictionnary = {}
    if request.method == 'POST':
        form = SolidareForm(request)
        dictionnary = form.values
        if form.is_valid:
            # Getting the place
            if form.values['country'] or form.values['postcode'] or\
                form.values['city'] or form.values['street'] or\
                form.values['streetnumber']:
                place = Place(country = form.values['country'], \
                    postcode = form.values['postcode'],\
                    city = form.values['city'], \
                    street = form.values['street'],\
                    number = form.values['streetnumber'])
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
            if form.values['type'] == 'offer':
                proposer = entity
            elif form.values['type'] == 'demand':
                demander = entity

            req = None
            # Filtered Request
            if form.values['filters'] == 'on':
                only_verified = True if form.values['verified'] == 'on' \
                            else False
                min_rating = DEF_MIN_RATING if form.values['min_rating'] == 'on'\
                            else 0
                gender = form.values['gender']

                req = FilteredRequest(name = form.values['description'],
                    date = date,
                    category = form.values['category'],
                    place = place,
                    proposer = proposer,
                    demander = demander,
                    state = Request.PROPOSAL)
                req.only_verified = only_verified
                req.min_rating = min_rating
                req.gender = gender
                req.save()

                age_filter = AgeFilter(min_age = form.values['min_age'],
                    max_age = form.values['max_age'],
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
                    state = Request.PROPOSAL)

            return redirect('account')

        else:
            dictionnary['errorlist'] = form.errorlist
            for key,value in form.colors.items():
                dictionnary[key] = value

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

                mess = InternalMessage(time=datetime.datetime.utcnow().replace(tzinfo=utc),
                                       sender=entity, request=Request.objects.get(id=req_id),
                                       message=request.POST.get('message-content'),
                                       receiver=Entity.objects.get(id=request.POST.get('receiver')))
                print(mess)
                mess.save()
            elif request.POST['type'] == "2":
                # Associate the current user with the request
                req.candidates.add(entity)
                req.save()

                #Force Open the modal
            elif request.POST['type'] == "3":
                messages = InternalMessage.objects.filter(request_id__exact=req_id).order_by('time')
                messages = map(lambda m: (sol_user(m.sender), sol_user(m.receiver), m.message, m.time, m.sender.id == entity.id or m.receiver.id == entity.id), messages)
                possible_rec = map(lambda r: sol_user(r), qs_add(qs_add(req.candidates, req.proposer), req.demander).exclude(id__exact=entity.id))
                print('ici')
                return render(request, 'message_display.html', {'request_id': req_id, 'messages': messages, 'possible_receivers' : possible_rec})

    threads = entity.get_all_requests(include_candidates=True).order_by('-date')
    threads = map(lambda t: (t.id, t.name, sol_user(InternalMessage.objects.filter(request_id__exact=t.id).order_by('-time').first().sender).picture if InternalMessage.objects.filter(request_id__exact=t.id).count() != 0 else None, ", ".join(map(lambda m: sol_user(m).__unicode__(), qs_add( qs_add(t.candidates, t.proposer), t.demander).exclude(id__exact=entity.id)))), threads)
    return render(request, 'messages.html', {'threads': threads})

@login_required
def exchanges(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        req_to_mod = Request.objects.get(id=req_id)
        req_to_mod.is_suspicious = True
        req_to_mod.save()
        



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




            if (elem.state == Request.PROPOSAL) and elem.candidates.all():
                demander = profile_current_offers( [elem] )[0][1]
                offer = profile_current_demands([elem])[0][1]
                candidate_req.append((elem,offer,demander))



            if (elem.state == Request.PROPOSAL) and not elem.candidates.all():
                demander = profile_current_offers( [elem] )[0][1]
                offer = profile_current_demands([elem])[0][1]
                posted_req.append((elem,offer,demander))




            if elem.state == Request.IN_PROGRESS:
                demander = profile_current_offers([elem])[0][1]
                offer = profile_current_demands([elem])[0][1]
                incoming_req.append((elem,offer,demander))

            #TODO FALSE
            if elem.state == Request.DONE and elem.get_feedback().rating_demander > 0:
                demander = profile_current_offers([elem])[0][1]
                offer = profile_current_demands([elem])[0][1]
                feedback_req.append((elem,offer,demander))




            if elem.state == Request.DONE and elem.get_feedback().rating_demander <= 0:
                demander = profile_current_offers([elem])[0][1]
                offer = profile_current_demands([elem])[0][1]
                realised_req.append((elem,offer,demander))


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

    if User.is_user(usr.id):
        usr_entity = User.objects.get(dj_user=usr.id)
    elif AssociationUser.is_assoc_user(usr.id):
        usr_entity = AssociationUser.objects.get(dj_user=usr.id).entity
    else:
        return redirect('login')
    searched = False
    max_times = 0
    if request.method == 'POST':
        search_field = request.POST['search']

        if 'search_saved' in request.POST.dict():
            if search_field == "":
                return render(request, 'search.html', {'search_saved_invalid': "True", 'search_results':search_results,
                                                     'max_times':max_times, 'searched':searched})
            else:
                pla = Place()
                pla.save()
                savedsearch = SavedSearch(place=pla, search_field=search_field, entity=usr_entity)
                savedsearch.save()
                return render(request, 'search.html', {'search_saved': "True", 'search_results':search_results,
                                                       'max_times':max_times, 'searched':searched})
        else:
            search_object = SavedSearch(search_field=search_field, category="Jardin")
            search_objects = usr_entity.search(search_object, 9)
            searched = True
            for this_request in search_objects:
                print(this_request)
                (req_initiator, req_type) = this_request.get_initiator()
                # Need to know if it's a User or a Association
                initiator_entity = sol_user(req_initiator)
                search_results.append((this_request, req_type, initiator_entity, this_request.place, this_request.date))
            max_times = len(search_results)
            return render(request, 'search.html', {'search_field': search_field, 'search_results':search_results,
                                                   'max_times':max_times, 'searched':searched})
    if request.method == 'GET':
        search_field = request.GET.get('id')
        if search_field:
            search_object = SavedSearch(search_field=search_field, category="Jardin")
            search_objects = usr_entity.search(search_object, 9)
            searched = True
            for this_request in search_objects:
                print(this_request)
                (req_initiator, req_type) = this_request.get_initiator()
                # Need to know if it's a User or a Association
                initiator_entity = sol_user(req_initiator)
                search_results.append((this_request, req_type, initiator_entity, this_request.place, this_request.date))
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


def sol_user(entity):
    if User.objects.filter(entity_ptr__exact=entity).count() != 0:
        return User.objects.get(entity_ptr=entity)
    elif Association.objects.filter(entity_ptr__exact=entity).count() != 0:
        return Association.objects.get(entity_ptr=entity)
    else:
        return entity


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
        print(form.type)
        return render(request, pages[type], dictionaries)


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
                                               last_name=form.name)

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
    usr = authenticate(username=form.user_name, password=form.passwd)
    Dlogin(request, usr)


    return redirect('account')


def handle_uploaded_file(f, filename, path):
    if f is not None:
        with open(path+'_'+filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
