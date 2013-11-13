# Class that represents a testimony on the Homepage
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 13 November 2013
# VERSION : 1
from django.db import models
import random

class Testimony(models.Model):
    testimony = models.CharField(max_length=512) # Value can be changed

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.testimony

    """ Get number testimonies chosen randomly in the database
        If there are less testimonies available in the database, return
        all the testimonies."""
    def get_random_testimonies(number):
        total = Testimony.objects.reverse()[:1].id
        if (number >= total):
            return Testimony.objects.all()
        # else, if number < total
        possible_values = range(1,total + 1) # [1, 2, ..., total-1, total]
        to_return = []
        for elem in range(number):
            chosen = random.choice(possible_values)
            #TODO TO BE CONTINUED


            
