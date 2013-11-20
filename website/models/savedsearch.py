# Class that represents a Saved Search done by an Entity
# AUTHOR :  Quentin De Coninck, Benjamin Baugnies, Anh Tuan Le
# DATE_CREATION : 16 November 2013
# DATE_VERSION 2: 19 November 2013
# DATE_VERSION 3: 20 November 2013
# VERSION : 3
from django.db import models
from place import *

class SavedSearch(models.Model):
    entity = models.ForeignKey('website.Entity')
    date = models.DateTimeField('date search', null=True, blank=True)
    search_field = models.CharField(max_length=512, null=True, blank=True)
    category = models.CharField(max_length=256, null=True, blank=True)
    place = models.ForeignKey(Place)
    
    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.search_field
