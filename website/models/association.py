# Class that represents a Association
# AUTHOR :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 23 November 2013
# VERSION : 1
from django.db import models
from entity import *
from associationuser import *

class Association(Entity):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return name

    # Return the list of the AssociationUser that work for self
    def get_employees(self):
        return AssociationUser.objects.filter(association__exact=self)

    # No reason to create a add_employee method, since the association variable
    # is mandatory in AssociationUser (but we can if it's useful somewhere...)
    
