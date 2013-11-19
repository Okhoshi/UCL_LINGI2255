# Class that represents a Saved Search done by an Entity
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 16 November 2013
# DATE_VERSION 2: 19 November 2013
# VERSION : 2
from django.db import models
from place import *
from entity import *

class SavedSearch(models.Model):
    entity = models.ForeignKey(Entity)
    date = models.DateTimeField('date search', null=True, blank=True)
    search_field = models.CharField(max_length=512, null=True, blank=True)
    category = models.CharField(max_length=256, null=True, blank=True)
    place = models.ForeignKey(Place)
    
    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.name
