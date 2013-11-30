# Class that represents a filter on the age
# AUTHOR :  Quentin De Coninck, Romain Vanwelde
# DATE_CREATION : 28 November 2013
# DATE_VERSION 1 : 30 November 2013
# VERSION : 1
from django.db import models
from django.utils.translation import ugettext_lazy as _

class AgeFilter(models.Model):
    min_age = models.IntegerField(default=-1, null=True, blank=True)
    max_age = models.IntegerField(default=-1, null=True, blank=True)
    filtered_request = models.ForeignKey('website.FilteredRequest')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return _("For FR") + filtered_request.__unicode__() + _("min: ") + \
               str(min_age) + _(" max: ") + str(max_age)
