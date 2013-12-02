# Class that represents a general user/actor (registered) of the website
# AUTHORS :  Anh Tuan Le, Romain Vanwelde, Benjamin Baugnies ,
#            Quentin De Coninck, Quentin Devos, Romain Vanwelde (V4)
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 19 November 2013
# DATE_VERSION 3 : 20 November 2013 
# DATE_VERSION 4 : 30 November 2013 
# VERSION : 4
from django.db import models
from place import *
from feedback import *
from internalmessage import *
from request import *
from savedsearch import *
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext as _

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
    def get_all_requests(self):
        proposed_request = Request.objects.filter(proposer__exact=self)

        demanded_request = Request.objects.filter(demander__exact=self)

        return proposed_request | demanded_request

    # Return a list of requests with the IN_PROGRESS state
    def get_current_requests(self):
        proposed_request = Request.objects.filter(state__exact=\
            Request.IN_PROGRESS).filter(proposer__exact=self)

        demanded_request = Request.objects.filter(state__exact=\
            Request.IN_PROGRESS).filter(demander__exact=self)

        return proposed_request | demanded_request

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

    # Return a list of the saved searches made by the entity
    def get_searches(self):
        return SavedSearch.objects.filter(entity__exact=self)

    # Return the rating of self based on the rating made by other entities met 
    # with done requests
    def  get_rating(self):
         # Get the feedbacks where Entity is the demander
        feedback_demand = Feedback.objects.filter(request__demander__exact=self)

        # Get the feedbacks where Entity is the proposer
        feedback_propos = Feedback.objects.filter(request__proposer__exact=self)

        total = 0.0

        for x in feedback_demand:
            total += x.rating_proposer

        for y in feedback_propos:
            total += y.rating_demander

        return total/(len(feedback_propos)+len(feedback_demand))

    # Return a list of requests with the DONE state
    def get_old_requests(self):
        proposed_request = Request.objects.filter(state__exact=\
            Request.DONE).filter(proposer__exact=self)

        demanded_request = Request.objects.filter(state__exact=\
            Request.DONE).filter(demander__exact=self)

        return proposed_request | demanded_request

    # Return a list of matching requests with the savedsearch
    def search(self, savedsearch):
        #TODO
        pass

    # Return a list of requests suggested by previous requests of self d
    def get_similar_matching_requests(self, amount):
        #TODO
        pass
