from django.contrib import admin
from website.models import *

class UserAdmin(admin.ModelAdmin):
    fields = ['dj_user', 'confirmed_status', 'id_card']
    list_display = ('dj_user', 'confirmed_status', 'id_card')
    list_filter = ['confirmed_status']

class AssocAdmin(admin.ModelAdmin):
    fields = ['dj_user', 'confirmed_status', 'id_card']
    list_display = ('dj_user', 'confirmed_status', 'id_card')
    list_filter = ['confirmed_status']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Place)
admin.site.register(Request)
admin.site.register(FilteredRequest)
admin.site.register(Testimony)
admin.site.register(Association)
admin.site.register(AssociationUser)
