from django import forms
from re import match
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class MForm(forms.Form):
    #Static variables
    ORG = True
    IND = False
    SOLIDAREITCOLOR = '#e1007a'

    def __init__(self, request):
        form = request.POST
        self.colors = dict()
        self.errorlist = dict()

        ### LAST NAME ###
        if form['name'] != ''and match(r"^[a-zA-Z ]*$", form['name']):
            self.name = form['name']
        else:
            self.is_valid = False
            self.colors['name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Name'] = _("This field can only contain uppercase and lowercase letters")

        ### FIRST NAME ###
        if form['first_name'] != '' and match(r"^[a-zA-Z ]*$", form['name']):
            self.first_name = form['first_name']
        else:
            self.is_valid = False
            self.colors['first_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['First name'] = _("This field can only contain uppercase and lowercase letters")

        ### USER NAME ###
        if form['user_name'] != '' and match(r"^.{3,15}$", form['user_name']):
            if User.objects.filter(username=form['user_name']).count() == 0:
                self.user_name = form['user_name']
            else:
                self.is_valid = False
                self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['User name'] = _("This username is already used")
        else:
            self.is_valid = False
            self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['User name'] = _("The username must be between 3 and 15 characters")


        ### EMAIL ###
        if form['email'] != '' and match(r"[^@]+@[^@]+\.[^@]+", form['email']):
            self.email = form['email']
        else:
            self.is_valid = False
            self.colors['email_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Email'] = _("Insert a valid email")
            
        ### PASSWORD ###
        if form['passwd'] == form['passwdC'] and form['passwd'] != ''\
                and match(r"^[A-Za-z0-9,;:=?./+-_)(]{4,20}$", form['passwd']):
            self.passwd = form['passwd']
        else:
            self.is_valid = False
            self.colors['passwd_color'] = MForm.SOLIDAREITCOLOR
            self.colors['passwdC_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Password'] = _("The password must be between 4 and 20 characters and only contain alphanumeric characters and the ',;:=?./+-_)('")
            
        ### ADDRESS ##
        if form['street'] != ''and match(r"^[a-zA-Z0-9 ]*$", form['name']):
            self.street = form['street']
        else:
            self.is_valid = False
            self.colors['street_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Street'] = _("This street") + " " +_("can only contain alphanumeric characters")

        if form['streetnumber'] != '' and match(r"^[0-9]{1,5}$", form['streetnumber']):
            self.streetnumber = form['streetnumber']
        else:
            self.is_valid = False
            self.colors['streetnumber_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Street number'] = _("The street number")+ " "+  _("is a number composed of 1 to 5 digits")
    
        if form['city'] != '' and match(r"^[a-zA-Z0-9 -_]*$", form['city']):
            self.city = form['city']
        else:
            self.is_valid = False
            self.colors['city_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['city'] = _("The city") + " " + _("can only contain alphanumeric characters or symbols")

                
        if form['country'] != '' and match(r"^[a-zA-Z0-9 -_]*$", form['country']):
            self.country = form['country']
        else:
            self.is_valid = False
            self.colors['country_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['country'] = _("The country") + " " + _("can only contain alphanumeric characters or symbols")
                
        if form['postcode'] != '' and match(r"^[0-9]{1,9}$", form['postcode']):
            self.postcode = form['postcode']
        else:
            self.is_valid = False
            self.colors['postcode_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['postcode'] = _("The post code") + " "+  _("is a number composed of 1 to 9 digits")

        self.facebook = form['facebook']

        if form.__contains__('org_name'):
            self.type = MForm.ORG

            if form['org_name'] != '' and match(r"^[A-Za-z0-9,;:=?./+-_]*$", form['org_name']):
                self.org_name = form['org_name']
            else:
                self.is_valid = False
                self.colors['org_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['org_name'] = _("The organisation name") + " "+ _("can only contain alphanumeric characters or symbols")
                
            
            if form['VAT'] == '' or match(r"^[A-Z0-9]*$", form['VAT']):
                self.VAT = form['VAT']
            else:
                self.is_valid = False
                self.colors['VAT_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['VAT'] = _("The VAT of the organisation") + " "+ _("can only contain alphanumeric characters")
            
            self.org_site = form['org_site']
            self.org_phone = form['org_phone']
            self.description = form['description']
            
        else:
            self.type = MForm.IND
            self.phone = form['phone']
            self.id_card = form['id_card']
