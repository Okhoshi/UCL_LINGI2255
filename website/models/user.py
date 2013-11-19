# Class that represents a User (non Association) of the website (registered)
# AUTHORS :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# VERSION : 1
from django.db import models
from django.contrib.auth.models import User as DUser
from website.models.entity import *


def pic_path(instance, filename):
    return 'profile_pic/' + (instance.first_name + instance.last_name).__hash__()


def id_path(instance, filename):
    return 'profile_pic/' + (instance.first_name + instance.last_name).__hash__()


class User(Entity, DUser):
    confirmed_status = models.BooleanField()
    picture = models.ImageField(upload_to=pic_path)
    id_card = models.ImageField(upload_to=id_path)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        #TODO
        return first_name + ' ' + last_name


    #TODO Add the methods here
