# Class that represents a general user/actor (registered) of the website
# AUTHORS :  Quentin De Coninck, Quentin Devos (V1)
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 19 November 2013
# VERSION : 2
from django.db import models
from place import *
from feedback import *

class Entity(models.Model):
    location = models.OneToOneField(Place)
    followed = models.ManyToManyField('self')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return "Entity contains no interesting information: call User or \
                association user instead"

    #TODO Add the methods here

    # Return a tuple (List of feedback "demander", List of feedback "proposer")
    def get_feedback(self):
        # Get the feedbacks where Entity is the demander
        feedback_demand = Feedback.objects.filter(request__demander__exact=self)

        # Get the feedbacks where Entity is the proposer
        feedback_propos = Feedback.objects.filter(request__proposer__exact=self)

        return (feedback_demand, feedback_propos)
