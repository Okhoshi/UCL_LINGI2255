# Class that represents a Association
# AUTHOR :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 23 November 2013
# VERSION : 1
from django.db import models
from website.models.entity import *
from website.models.associationuser import *

def pic_path(instance, filename):
    return 'profile_pic/' + instance.__unicode__().__hash__()

class Association(Entity):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    picture = models.ImageField(upload_to=pic_path)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.name

    # Return the list of the AssociationUser that work for self
    def get_employees(self):
        return AssociationUser.objects.filter(entity__exact=self)

    # No reason to create a add_employee method, since the association variable
    # is mandatory in AssociationUser (but we can if it's useful somewhere...)
    
