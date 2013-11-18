# Class that represents a Association
# AUTHOR :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# VERSION : 1
from django.db import models
from entity import *

class Association(Entity):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return name

    #TODO Add the methods here
    
