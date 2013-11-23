# Class that represents a member of an Association
# AUTHOR :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 18 November 2013
# VERSION : 1
from django.db import models
from django.contrib.auth.models import User
from pin import *

class AssociationUser(User):
    level = models.IntegerField()
    association = models.ForeignKey('website.Association')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return first_name + ' ' + last_name + ' (' + association.name + ')'

    #TODO Add the methods here
    
