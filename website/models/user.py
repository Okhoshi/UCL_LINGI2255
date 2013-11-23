# Class that represents a User (non Association) of the website (registered)
# AUTHORS :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1 : 18 November 2013
# DATE_VERSION 2 : 23 November 2013
# VERSION : 2
from django.db import models
from django.contrib.auth.models import User as DUser
from website.models.entity import *


class SIUserManager(models.Manager):

    @staticmethod
    def create_user(username, email, password, **extra_field):
        buser = DUser.objects.create_user(username, email, password,
                                          first_name=extra_field.get('first_name', ''),
                                          last_name=extra_field.get('last_name', ''))
        user = User()
        user.user = buser
        user.confirmed_status = extra_field.get('confirmed_status', False)
        user.location = extra_field.get('location')
        user.save()
        return user


def pic_path(instance, filename):
    return 'profile_pic/' + instance.__unicode__().__hash__()


def id_path(instance, filename):
    return 'id_pic/' + instance.__unicode__().__hash__()


class User(Entity):
    user = models.OneToOneField(DUser)
    confirmed_status = models.BooleanField()
    picture = models.ImageField(upload_to=pic_path)
    id_card = models.ImageField(upload_to=id_path)
    objects = SIUserManager()

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

    #TODO Add the methods here
    def is_verified(self):
        return self.confirmed_status
