# Class that represents a place (location) for an Entity or a Request
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 16 November 2013
# DATE_VERSION 2: 19 November 2013
# VERSION : 2
from django.db import models

class Place(models.Model):
    country = models.CharField(max_length=128, null=True, blank=True) # Even lower size?
    city = models.CharField(max_length=128, null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    number = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.country + ", " + self.city + ", " + self.street + ", " + \
               str(self.number)