# Class that represents a general user/actor (registered) of the website
# AUTHORS :  Quentin De Coninck, Quentin Devos (V1)
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# VERSION : 1
from django.db import models
from place import *
from savedsearch import *
from internalmessage import *
from feedback import *
from request import *

class Entity(models.Model):
    location = models.OneToOneField(Place)
    followed = models.ManyToManyField('self')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO ?
        return name

    #TODO Add the methods here