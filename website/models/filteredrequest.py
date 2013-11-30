# Class that represents a request where a filter is placed
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 28 November 2013
# DATE_VERSION 1 : 30 November 2013
# VERSION : 1
from request import *
from agefilter import *
from django.utils.translation import ugettext_lazy as _

class FilteredRequest(Request):

    MAN = 'M'
    WOMAN = 'W'
    
    GENDER_CHOICES = (
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
    )
    
    only_verified = models.BooleanField(default=False)
    min_rating = models.IntegerField(default=0, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, \
                             blank=True)

    class Meta:
        app_label = 'website'
    
    def __unicode__(self):
        return super(Request, self).__unicode__() + " " + _("filtered")

    # Return a list of the AgeFilters of the FilteredRequest
    # If no AgeFilter is linked to FilteredRequest, then return an empty list
    def get_age_filter(self):
        to_return = []
        af = AgeFilter.objects.filter(filtered_request__exact=self)
        if af:
            for elem in af:
                to_return.append(elem)

        return to_return
