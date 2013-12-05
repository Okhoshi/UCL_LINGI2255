# Class that represents a member of an Association
# AUTHOR :  Quentin De Coninck, Quentin Devos
# DATE_CREATION : 17 November 2013
# DATE_VERSION 1: 18 November 2013
# DATE_VERSION 2: 24 November 2013
# VERSION : 2
from django.db import models
from django.contrib.auth.models import User
from pin import *

class SIAssocUserManager(models.Manager):

    @staticmethod
    def create_user(username, email, password, association, level, **extra_field):
        buser = User.objects.create_user(username, email, password,
                                          first_name=extra_field.get('first_name', ''),
                                          last_name=extra_field.get('last_name', ''))
        user = AssociationUser()
        user.dj_user = buser
        user.entity = association
        user.level = level
        user.save()
        return user

    
def pic_path(instance, filename):
    return 'pic/' + str(instance.__unicode__().__hash__()) + filename


class AssociationUser(models.Model):

    MAN = 'M'
    WOMAN = 'W'
    UNSPECIFIED = 'U'

    GENDER_CHOICES = (
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
        (UNSPECIFIED, 'Unspecified'),
    )

    dj_user = models.OneToOneField(User, related_name='profile_a')
    level = models.IntegerField()
    entity = models.ForeignKey('website.Association')
    picture = models.ImageField(upload_to=pic_path)
    objects = SIAssocUserManager()
    birth_day = models.DateTimeField('birth day')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return self.dj_user.first_name + ' ' + self.dj_user.last_name + \
               ' (' + self.entity.name + ')'

    # get_level : useless since level is a instance variable

    # Return the PINs managed by self
    def get_pin(self):
        return PIN.objects.filter(managed_by__exact=self)

    # Create a new PIN that will be managed by self and save it in database
    def set_pin(self, first_name, last_name):
        pin = PIN(first_name=first_name, last_name=last_name, managed_by=self)
        pin.save()

    # Transfert the pin from self to other_au.
    # In other words, pin.managed_by = other_au after this method
    # Notice that this method prevents a pin to be moved if pin is not managed
    # by self.
    def transfer_pin(self, pin, other_au):
        if (pin.managed_by == self):
            pin.managed_by = other_au

    # get_association
    def get_association(self):
        return self.entity
    # get_association_user: not useful (why using a ID??)
    
    @staticmethod
    def is_assoc_user(user_id):
        return AssociationUser.objects.filter(dj_user__exact=user_id).count() == 1