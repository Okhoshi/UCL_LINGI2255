# Class that represents a Person In Need, helped by an Association(User)
# AUTHOR :  Quentin De Coninck, Benjamin Baugnies, Anh Tuan Le, Romain Vanwelde
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 19 November 2013
# DATE_VERSION 2: 20 November 2013
# DATE_VERSION 3 : 30 November 2013
# VERSION : 3
from django.db import models
from django.utils.translation import ugettext_lazy as _

class PIN(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    managed_by = models.ForeignKey('website.AssociationUser', related_name='manager_of')

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
