# Class that represents a message between two Entities about a Request
# AUTHOR :  Quentin De Coninck, Anh Tuan Le
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# VERSION : 1
from django.db import models
from django.utils.translation import ugettext as _
#from entity import *
#from request import *

class InternalMessage(models.Model):
    time = models.DateTimeField('date message')
    sender = models.ForeignKey('website.Entity', related_name='sended')
    request = models.ForeignKey('website.Request')
    message = models.CharField(max_length=2048)
    receiver = models.ForeignKey('website.Entity', related_name='received')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return _("From: ") + self.sender.__unicode__() + " " + \
               _("To: ") + self.receiver.__unicode__() + " " + \
               _("Message: ") + self.message

    
