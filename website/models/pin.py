# Class that represents a Person In Need, helped by an Association(User)
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 17 November 2013
# VERSION : 1
from django.db import models
from associationuser import *

class PIN(models.Model):
    #TODO Add the instance variables here

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return "TODO"

    #TODO Add the methods here
    
