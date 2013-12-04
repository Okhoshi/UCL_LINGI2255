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
        user.dj_user = buser
        user.confirmed_status = extra_field.get('confirmed_status', False)
        user.location = extra_field.get('location')
        user.birth_day = extra_field.get('birth_day')
        user.gender = extra_field.get('gender')
        user.save()
        return user


def pic_path(instance, filename):
    return 'pic/' + str(instance.__unicode__().__hash__()) + filename


def id_path(instance, filename):
    return 'id_card/' + str(instance.__unicode__().__hash__()) + filename


class User(Entity):
    MAN = 'M'
    WOMAN = 'W'
    UNSPECIFIED = 'U'

    GENDER_CHOICES = (
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
        (UNSPECIFIED, 'Unspecified'),
    )

    dj_user = models.OneToOneField(DUser, related_name='profile')
    confirmed_status = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=pic_path)
    id_card = models.ImageField(upload_to=id_path)
    birth_day = models.DateTimeField('birth day')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    objects = SIUserManager()

    class Meta:
        app_label = 'website'

    def __init__(self, *args, **kwargs):
        u = super(User, self).__init__(*args, **kwargs)
        self.entity = self
        return u
    
    def __unicode__(self):
        return self.dj_user.first_name + ' ' + self.dj_user.last_name

    # Return True is the user was verified by the administrator of Solidare-IT
    def is_verified(self):
        return self.confirmed_status

    @staticmethod
    def is_user(user_id):
        return User.objects.filter(dj_user__exact=user_id).count() == 1
