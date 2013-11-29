# Class that represents a feedback about an Request between two Entities
# AUTHOR :  Quentin De Coninck, Anh Tuan Le
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# VERSION : 1
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from request import *

class Feedback(models.Model):
    feedback_demander = models.CharField(max_length=2048, null=True, blank=True)
    feedback_proposer = models.CharField(max_length=2048, null=True, blank=True)
    request = models.OneToOneField('website.Request')
    rating_demander = models.IntegerField(default=0, null=True, blank=True)
    rating_proposer = models.IntegerField(default=0, null=True, blank=True)    

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return _("Feedback about ") + self.request.__unicode__()
