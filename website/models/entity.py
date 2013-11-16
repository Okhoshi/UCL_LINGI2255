# Class that represents a general user/actor (registered) of the website
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 17 November 2013
# VERSION : 1
from django.db import models
from place import *
from savedsearch import *
from internalmessage import *
from feedback import *
from request import *

class Entity(models.Model):
    #TODO Add the instance variables here

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return "TODO"

    #TODO Add the methods here
