# Class that represents a feedback about an Request between two Entities
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 17 November 2013
# VERSION : 1
from django.db import models
from entity import *
from request import *

class Feedback(models.Model):
    #TODO Add the instance variables here

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return "TODO"

    #TODO Add the methods here
