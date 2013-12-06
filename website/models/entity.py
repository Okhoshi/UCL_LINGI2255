# Class that represents a general user/actor (registered) of the website
# AUTHORS :  Anh Tuan Le, Romain Vanwelde, Benjamin Baugnies ,
#            Quentin De Coninck, Quentin Devos, Romain Vanwelde (V4)
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 19 November 2013
# DATE_VERSION 3 : 20 November 2013 
# DATE_VERSION 4 : 30 November 2013 
# DATE_VERSION 5 : 3 December 2013
# VERSION : 5
from django.db import models
from place import *
from feedback import *
from internalmessage import *
from request import *
from savedsearch import *
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.db.models import Q


class Entity(models.Model):
    location = models.OneToOneField(Place)
    followed = models.ManyToManyField('self')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return _("Entity contains no interesting information: call User or \
                association user instead")

    #TODO Add the methods here

    # Return a tuple (List of feedback "demander", List of feedback "proposer")
    def get_feedback(self):
        # Get the feedbacks where Entity is the demander
        feedback_demand = Feedback.objects.filter(request__demander__exact=self)

        # Get the feedbacks where Entity is the proposer
        feedback_propos = Feedback.objects.filter(request__proposer__exact=self)

        return (feedback_demand, feedback_propos)

    # Return a List of internal messages corresponding to the request
    def get_internal_messages(self, request):
        return InternalMessage.objects.filter(request__exact=request)

    # Return a list of all the requests made by the Entity
    def get_all_requests(self, include_candidates = False):
        proposed_request = Request.objects.filter(proposer__exact=self)

        demanded_request = Request.objects.filter(demander__exact=self)

        if include_candidates:
            candidates_request = Request.objects.filter(candidates__exact=self)
        else:
            candidates_request = Request.objects.none()

        return (proposed_request | demanded_request | candidates_request).distinct()

    # Return a list of requests with the IN_PROGRESS state
    def get_current_requests(self):
        proposed_request = Request.objects.filter(state__exact=\
            Request.IN_PROGRESS).filter(proposer__exact=self).order_by( \
            'date')

        demanded_request = Request.objects.filter(state__exact=\
            Request.IN_PROGRESS).filter(demander__exact=self).order_by( \
            'date')

        return proposed_request | demanded_request

    # Return a list of requests where self is the proposer and is not done
    def get_current_offers(self):
        return Request.objects.all().exclude(state__exact=\
            Request.DONE).filter(proposer__exact=self)

    # Return a list of requests where self is the demander and is not done
    def get_current_demands(self):
        return Request.objects.all().exclude(state__exact=\
            Request.DONE).filter(demander__exact=self)

    # Create an internal message about request with text to destination_entity
    # and saves it in the database
    def send_internal_message(self, request, text, destination_entity):
        msg = InternalMessage(time=\
            datetime.datetime.utcnow().replace(tzinfo=utc), message=text, \
            sender=self, receiver=destination_entity, request=request)
        msg.save()

    # Return the list of the entities followed by self
    def get_followed(self):
        return self.followed.all()

    # Add new_followed as entity followed by self
    def set_followed(self, new_followed):
        self.followed.add(new_followed)

    # Remove the old follow of the followed by self
    def remove_followed(self, old_followed):
        self.followed.remove(old_followed)
        self.save()

    # Return a list of the saved searches made by the entity
    def get_searches(self):
        return SavedSearch.objects.filter(entity__exact=self)

    # Return a tuple with the number of positive, negative and total requests based
    # on the feedbacks made by the others
    # Return (pos, neg, neu)
    def  get_rating(self):
         # Get the feedbacks where Entity is the demander
        feedback_demand = Feedback.objects.filter(request__demander__exact=self)

        # Get the feedbacks where Entity is the proposer
        feedback_propos = Feedback.objects.filter(request__proposer__exact=self)

        pos = 0
        neg = 0
        neu = 0

        for x in feedback_demand:
            if (x.rating_proposer == 3):
                pos += 1
            elif (x.rating_proposer == 1):
                neg += 1
            elif (x.rating_proposer == 2):
                neu += 1


        for y in feedback_propos:
            if (y.rating_demander == 3):
                pos += 1
            elif (y.rating_demander == 1):
                neg += 1
            elif (y.rating_demander == 2):
                neu += 1

        return (pos, neg, neu)

    # Return a list of requests with the DONE state
    def get_old_requests(self):
        proposed_request = Request.objects.filter(state__exact=\
            Request.DONE).filter(proposer__exact=self)

        demanded_request = Request.objects.filter(state__exact=\
            Request.DONE).filter(demander__exact=self)

        return proposed_request | demanded_request

    # Return a list of 'amount' matching requests with the savedsearch
    def search(self, savedsearch, amount, category_filter=False):
        
        searchfield = savedsearch.search_field.split(' ')
        
        requests = Request.objects.filter(state__exact = \
            Request.PROPOSAL).filter(~Q(proposer__exact=self), ~Q(demander__exact=self), ~Q(candidates__exact=self))
        if category_filter:
            requests = requests.filter(category__exact = \
            savedsearch.category)
        requests = requests.filter(reduce(lambda x, y: x | y,\
                [Q(name__icontains=word) for word in searchfield]))

        
   
        relevance = []
        for req in requests:
            tmp = 0
            for word in searchfield:
                if (word in req.name):
                    tmp += 1
            relevance.append([tmp, req])
            
        relevance.sort()
        relevance.reverse()
        if (len(relevance)>amount):
            relevance = relevance[:amount]
        requests = []
        for i in relevance:
            requests.append(i[1])
               
            
        return requests 

    # Return a list of 'amount' requests suggested by previous requests of self
    # uses full history
    def get_similar_matching_requests(self, amount):
        dreq = Request.objects.filter(state__exact = Request.DONE)
        requests = dreq.filter(demander__exact = self) | \
                   dreq.filter(proposer__exact = self)

        if (len(requests) == 0):
            return requests


        wordl = []
        catl = []
        for req in requests:
            name = req.name
            name = name.split(' ')
            wordl += name
            catl.append(req.category)
        wordl.sort()
        catl.sort()

        curword = wordl[0]
        mostused= []
        tmp = 1
        for i in range(1, len(wordl)):
            if (wordl[i] == curword):
                tmp += 1
            else :
                if (len(curword)>2):
                    mostused.append([tmp, curword])
                curword = wordl[i]
                tmp = 1
        mostused.append([tmp, curword])
        curword = catl[0]
        tmp = 1
        bestcat = []
        for i in range(1, len(catl)):
            if (catl[i] == curword):
                tmp += 1
            else :
                bestcat.append([tmp, curword])
                curword = catl[i]
                tmp = 1
        bestcat.append([tmp, curword])

        mostused.sort()
        mostused.reverse()
        bestcat.sort()
        bestcat.reverse()
        bestcat=bestcat[:3]
        searchfield = ''
        tmp = 0

        while (len(searchfield) < 512 and tmp < len(mostused)):
            for i in range(mostused[tmp][0]):
                searchfield += mostused[tmp][1] + ' '
            tmp += 1

        pla = Place()

        if (len(bestcat) == 3):
            if (amount%3 == 0):
                bestcat[0][0]=amount/3
                bestcat[1][0]=amount/3
                bestcat[2][0]=amount/3
            if (amount%3 == 1):
                bestcat[0][0]=amount/3+1
                bestcat[1][0]=amount/3
                bestcat[2][0]=amount/3
            if (amount%3 == 2):
                bestcat[0][0]=amount/3+1
                bestcat[1][0]=amount/3+1
                bestcat[2][0]=amount/3
        elif (len(bestcat)==2):
            if (amount%2 == 0):
                bestcat[0][0]=amount/2
                bestcat[1][0]=amount/2
            else :
                bestcat[0][0]=amount/2+1
                bestcat[1][0]=amount/2
        elif (len(bestcat) == 1):
            bestcat[0][0]=amount

        
        requests = []

        for i in range(len(bestcat)):
            savedsearch = SavedSearch(place = pla, date=\
                datetime.datetime.utcnow().replace(tzinfo=utc), search_field=\
                searchfield, category=bestcat[i][1], entity=self)
            
            tmp = self.search(savedsearch, bestcat[i][0], True)
            if (len(tmp)<bestcat[i][0] and (i+1)< len(bestcat)):
                bestcat[i+1][0] += (bestcat[i][0]-len(tmp))
            requests += tmp

        return requests
