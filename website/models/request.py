# Class that represents a Request of an Entity, that is looking for something
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 17 November 2013
# VERSION : 1
from django.db import models
from feedback import *
from internalmessage import *
from entity import *
from place import *

class Request(models.Model):
    #TODO Add the instance variables here

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return "TODO"

    #TODO Add the methods here
    
