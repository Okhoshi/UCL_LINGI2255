# Class that represents a Request of an Entity, that is looking for something
# AUTHOR :  Quentin De Coninck, Anh Tuan Le
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# VERSION : 1
from django.db import models
from entity import *
from place import *
from pin import *

class Request(models.Model):
    PROPOSAL = 'P'
    IN_PROGRESS = 'I'
    DONE = 'D'
    
    STATUS_CHOICES = (
        (PROPOSAL, 'Progress'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
    )
    
    #TODO Add the instance variables here
    name = models.CharField(max_length=512)
    date = models.DateTimeField('request date', null=True, blank=True)
    category = models.CharField(max_length=256)
    place = models.ForeignKey(Place)
    proposer = models.ForeignKey(Entity, related_name='proposed', null=True, \
                                 blank=True)
    demander = models.ForeignKey(Entity, related_name='demanded', null=True, \
                                 blank=True)
    candidates = models.ManyToManyField(Entity, related_name='candidated', \
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
        #TODO
        return "TODO"

    #TODO Add the methods here
    
