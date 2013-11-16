# Class that represents a Saved Search done by an Entity
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 16 November 2013
# VERSION : 1
from django.db import models
from place import *

class SavedSearch(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField('date search', null=True, blank=True)
    search_field = models.CharField(max_length=400, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True)
    
    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.name
