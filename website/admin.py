from django.contrib import admin
from website.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Place)
admin.site.register(Request)
admin.site.register(FilteredRequest)
admin.site.register(Association)
admin.site.register(AssociationUser)
