# Class that represents a request where a filter is placed
# AUTHOR :  Quentin De Coninck
# DATE_CREATION : 28 November 2013
# DATE_VERSION 1 : 30 November 2013
# VERSION : 1
from request import *
from agefilter import *
from django.utils.translation import ugettext as _

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
        return self.name + " " + _("filtered")

    # Return a list of the AgeFilters of the FilteredRequest
    # If no AgeFilter is linked to FilteredRequest, then return an empty list
    def get_age_filter(self):
        to_return = []
        af = AgeFilter.objects.filter(filtered_request__exact=self)
        if af:
            for elem in af:
                to_return.append(elem)

        return to_return

    # Return all requests that are public, i.e. that don't have filters on it
    # It means that the request returned are only Requests (and not FilteredRequests)
    @staticmethod
    def get_all_public_requests():
        req = Request.objects.all()
        return req.exclude(filteredrequest__in=[o for o in req])

    @staticmethod
    def get_latest_requests(amount):
        return FilteredRequest.get_all_public_requests().order_by('-date')[:amount]
