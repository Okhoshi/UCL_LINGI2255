from django import forms
from re import match
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from recaptcha.client import captcha
from django.conf import settings


class SolidareForm(forms.Form):
    SOLIDAREITCOLOR = '#e1007a'
    def __init__(self,request):
        form = request.POST
        self.colors = dict()
        self.errorlist = dict()

        self.is_valid = True

        myType = request.POST.get('type')
        date = request.POST.get('date')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        category = request.POST.get('category')
        description = request.POST.get('description')

        print(myType,date,city,postcode,category,description)

# Form to add representatives
class RForm(forms.Form):
    SOLIDAREITCOLOR = '#e1007a'

    def __init__(self, request):
        form = request.POST
        self.colors = dict()
        self.errorlist = dict()

        self.is_valid = True

        last_names = request.POST.getlist('last_name[]')
        first_names = request.POST.getlist('first_name[]')
        emails = request.POST.getlist('email[]')
        levels = request.POST.getlist('memberLevel[]')

        self.rows = []
        for index,_ in enumerate(last_names):
            row = {}
            isEmpty = True
            if last_names[index] and match(r"^[a-zA-Z ]*$", last_names[index]):
                row['last_name'] = last_names[index]
                isEmpty = False
            else:
                row['last_name'] = u''
                row['last_name_color'] = MForm.SOLIDAREITCOLOR
                self.is_valid = False
                self.errorlist['Name'] = "This field can only contain uppercase and lowercase letters"

            if first_names[index] and match(r"^[a-zA-Z ]*$", first_names[index]):
                row['first_name'] = first_names[index]
                isEmpty = False
            else:
                row['first_name'] = u''
                row['first_name_color'] = MForm.SOLIDAREITCOLOR
                self.is_valid = False
                self.errorlist['First name'] = "This field can only contain uppercase and lowercase letters"

            if emails[index] and match(r"[^@]+@[^@]+\.[^@]+", emails[index]):
                row['email'] = emails[index]
                isEmpty = False
            else:
                row['email'] = u''
                row['email_color'] = MForm.SOLIDAREITCOLOR
                self.is_valid = False
                self.errorlist['Email'] = "Insert a valid email" # TODO : TRADUIRE ET AJOUTER _() !!

            if levels[index] != '' and match(r"^[0-9]{1,9}$", levels[index]):
                row['level'] = levels[index]
            else:
                row['level'] = u''
                row['level_color'] = MForm.SOLIDAREITCOLOR
                self.is_valid = False
                self.errorlist['Level'] = "The level should be a number"

            if not isEmpty:
                self.rows.append(row)

class MForm(forms.Form):
    #Static variables
    ORG = True
    IND = False
    SOLIDAREITCOLOR = '#e1007a'

    def __init__(self, request):
        form = request.POST
        self.colors = dict()
        self.errorlist = dict()
        ### CAPTCHA ###
        response = captcha.submit(form.get('recaptcha_challenge_field'),
                                  form.get('recaptcha_response_field'),
                                  settings.RECAPTCHA_PRIVATE_KEY,
                                  request.META.get('REMOTE_ADDR'))
        if not response.is_valid:
            self.errorlist[_("Captcha")] = _("The captcha is invalid")

        self.is_valid = response.is_valid

        ### LAST NAME ###
        if form.get('name', '') != '' and match(r"^[a-zA-Z ]*$", form.get('name', '')):
            self.name = form.get('name', '')
        else:
            self.is_valid = False
            self.colors['name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Name")] = _("This field can only contain uppercase and lowercase letters")

        ### FIRST NAME ###
        if form.get('first_name', '') != '' and match(r"^[a-zA-Z ]*$", form.get('first_name', '')):
            self.first_name = form.get('first_name', '')
        else:
            self.is_valid = False
            self.colors['first_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("First name")] = _("This field can only contain uppercase and lowercase letters")

        ### BIRTHDATE ###
        if form.get('birthdate', '') != '':
            self.birthdate = form.get('birthdate', '')
        else:
            self.is_valid = False
            self.colors['birthdate_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Birthdate")] = _("This field can only contain a birthdate")

        self.gender = form.get('gender')

        ### USER NAME ###
        if form.get('user_name', '') != '' and match(r"^.{3,15}$", form.get('user_name', '')):
            if User.objects.filter(username=form.get('user_name', '')).count() == 0:
                self.user_name = form.get('user_name', '')
            else:
                self.is_valid = False
                self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist[_("User name")] = _("This username is already used")
        else:
            self.is_valid = False
            self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("User name")] = _("The username must be between 3 and 15 characters")


        ### EMAIL ###
        if form.get('email', '') != '' and match(r"[^@]+@[^@]+\.[^@]+", form.get('email', '')):
            self.email = form.get('email', '')
        else:
            self.is_valid = False
            self.colors['email_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Email")] = _("Insert a valid email")
            
        ### PASSWORD ###
        if form.get('passwd', '') == form.get('passwdC', '') and form.get('passwd', '') != ''\
                and match(r"^[A-Za-z0-9,;:=?./+-_)(]{4,20}$", form.get('passwd', '')):
            self.passwd = form.get('passwd', '')
        else:
            self.is_valid = False
            self.colors['passwd_color'] = MForm.SOLIDAREITCOLOR
            self.colors['passwdC_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Password")] = _("The password must be between 4 and 20 characters and only contain alphanumeric characters and the ',;:=?./+-_)('")

        ### ADDRESS ##
        if form.get('street', '') != ''and match(r"^[a-zA-Z0-9 ]*$", form.get('street', '')):
            self.street = form.get('street', '')
        else:
            self.is_valid = False
            self.colors['street_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Street")] = _("This street") + " " +_("can only contain alphanumeric characters")

        if form.get('streetnumber', '') != '' and match(r"^[0-9]{1,5}$", form.get('streetnumber', '')):
            self.streetnumber = form.get('streetnumber', '')
        else:
            self.is_valid = False
            self.colors['streetnumber_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Street number")] = _("The street number")+ " "+  _("is a number composed of 1 to 5 digits")
    
        if form.get('city', '') != '' and match(r"^[a-zA-Z0-9 -_]*$", form.get('city', '')):
            self.city = form.get('city', '')
        else:
            self.is_valid = False
            self.colors['city_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("City")] = _("The city") + " " + _("can only contain alphanumeric characters or symbols")
                
        if form.get('country', '') != '' and match(r"^[a-zA-Z0-9 -_]*$", form.get('country', '')):
            self.country = form.get('country', '')
        else:
            self.is_valid = False
            self.colors['country_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Country")] = _("The country") + " " + _("can only contain alphanumeric characters or symbols")
                
        if form.get('postcode', '') != '' and match(r"^[0-9]{1,9}$", form.get('postcode', '')):
            self.postcode = form.get('postcode', '')
        else:
            self.is_valid = False
            self.colors['postcode_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist[_("Postcode")] = _("The post code") + " "+  _("is a number composed of 1 to 9 digits")

        self.facebook = form.get('facebook', '')

        if form.__contains__('org_name'):
            self.type = MForm.ORG

            if form.get('org_name', '') != '' and match(r"^[A-Za-z0-9,;:=?./+-_]*$", form.get('org_name', '')):
                self.org_name = form.get('org_name', '')
            else:
                self.is_valid = False
                self.colors['org_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist[_("Organisation name")] = _("The organisation name") + " "+ _("can only contain alphanumeric characters or symbols")

            self.org_site = form.get('org_site', '')
            self.org_phone = form.get('org_phone', '')
            self.description = form.get('description', '')
            
        else:
            self.type = MForm.IND
            self.phone = form.get('phone', '')
            self.id_card = form.get('id_card', '')
