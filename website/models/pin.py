# Class that represents a Person In Need, helped by an Association(User)
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# VERSION : 1
from django.db import models
from associationuser import *

class PIN(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    managed_by = models.ForeignKey(AssociationUser)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return 'PIN first name: ' + self.first_name + ', last name: ' + \
               self.last_name
