# Class that represents a testimony on the Homepage
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 13 November 2013
# DATE_VERSION2 : 15 November 2013
# VERSION : 2
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
    @staticmethod
    def get_random_testimonies(number):
        # It would be not the best implementation, thought it will works
        # 1 Go fetch all the Testimonies
        # 2 Choose randomly number Testimonies to return
        testimonies = list(Testimony.objects.all())
        total = Testimony.objects.count()
        if (number >= total):
            return testimonies
        # else
        to_return = []
        for counter in range(number):
            chosen = random.choice(testimonies)
            to_return.append(chosen)
            testimonies.remove(chosen)
        return to_return


            
