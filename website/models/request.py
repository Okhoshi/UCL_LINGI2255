# Class that represents a Request of an Entity, that is looking for something
# AUTHOR :  Quentin De Coninck, Anh Tuan Le
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# DATE_VERSION 2: 20 November 2013
# VERSION : 2
from django.db import models
from place import *
from pin import *
from django.utils.translation import ugettext as _

class Request(models.Model):
    PROPOSAL = 'P'
    IN_PROGRESS = 'I'
    DONE = 'D'
    
    STATUS_CHOICES = (
        (PROPOSAL, 'Proposal'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
    )
    
    name = models.CharField(max_length=512)
    date = models.DateTimeField('request date', null=True, blank=True)
    category = models.CharField(max_length=256)
    place = models.ForeignKey(Place)
    proposer = models.ForeignKey('website.Entity', related_name='proposed', null=True, \
                                 blank=True)
    demander = models.ForeignKey('website.Entity', related_name='demanded', null=True, \
                                 blank=True)
    candidates = models.ManyToManyField('website.Entity', related_name='candidated', \
                                        null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATUS_CHOICES, \
                             default=PROPOSAL)
    is_suspicious = models.BooleanField(default=False)    
    pin_demander = models.ForeignKey(PIN, related_name='demanded', null=True, \
                                     blank=True)
    pin_proposer = models.ForeignKey(PIN, related_name='proposed', null=True, \
                                     blank=True)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.name

    #TODO Add the methods here

    # Return the feedback associated to the request
    def get_feedback(self):
        return self.feedback

    # Return all the requests in the database
    @staticmethod
    def get_all_requests():
        return Request.objects.all()

    

    # Return some requests that are similar with self
    def get_similar_requests(self):
        # SHOULD BE REDONE!!!
        # Search similar names and type
        set1 = Request.objects.filter(name__icontains=self.name)
        set2 = Request.objects.filter(category__icontains=self.category)
        # Merge and distinct
        great_set = set1 | set2
        great_set_return = great_set
        # Fetch requests with same locality
        loc1 = None
        loc2 = None
        loc3 = None
        if (self.place.country != None):
            loc1 = Place.objects.filter(country__icontains=self.place.country)
            loc3 = loc1
        if (self.place.city != None):
            loc2 = Place.objects.filter(city__icontains=self.place.city)
            loc3 = loc2
        if (loc1 and loc2):
            loc3 = loc1 | loc2
        if (loc3):
            set3 = reduce(operator.and_, (Q(place__contains=x) \
                                          for x in loc3))
            great_set_return = great_set | set3
        return great_set_return

    # Should be used when sending a message or viewing the profile of initiator
    # Return a tuple with the demander and the tag (P or D) of proposal or demand
    def get_initiator(self):
        # Only useful when it's a proposal
        if (self.state != Request.PROPOSAL):
            return None
        if (self.demander != None):
            return (self.demander, _('Demand'))
        # else, it's the proposer
        return (self.proposer, _('Proposal'))

    # Allows a user to create a request with a SavedSearch as basis.
    # If the request is as proposal, isProposer must be True, else False
    @staticmethod
    def make_request(search, isProposer):
        new = Request(name=search.search_field, date=search.date, \
                      category=search.category, place=search.place)
        if (isProposer):
            new.proposer = search.entity
        else:
            new.demander = search.entity

        new.save()
        return new
    
            
            
        
