from django import forms
from re import match

class MForm(forms.Form):
    #Static variables
    ORG = True
    IND = False
    SOLIDAREITCOLOR = '#e1007a'

    def __init__(self, request):
        form = request.POST
        self.colors = dict()
        if form.__contains__('organisation'):
            self.type = MForm.ORG
        else:
            self.type = MForm.IND

            ### NAME ###
            if form['name'] != ''and match(r"^[a-zA-Z ]*$", form['name']):
                self.name = form['name']
            else:
                self.is_valid = False
                self.colors['name_color'] = MForm.SOLIDAREITCOLOR

            ### FIRST NAME ###
            if form['first_name'] != '' and match(r"^[a-zA-Z ]*$", form['name']):
                self.first_name = form['first_name']
            else:
                self.is_valid = False
                self.colors['first_name_color'] = MForm.SOLIDAREITCOLOR

            ### USER NAME ###
            if form['user_name'] != '' and match(r"^.{3,15}$", form['user_name']):
                self.user_name = form['user_name']
            else:
                self.is_valid = False
                self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR

            ### EMAIL ###
            if form['email'] != '' and match(r"[^@]+@[^@]+\.[^@]+", form['email']):
                self.email = form['email']
            else:
                self.is_valid = False
                self.colors['email_color'] = MForm.SOLIDAREITCOLOR
            
            ### PASSWORD ###
            if form['passwd'] == form['passwdC'] and form['passwd'] != ''\
                    and match(r"^[A-Za-z0-9,;:=?./+-_)(]{4,20}$", form['user_name']):
                self.passwd = form['passwd'].__hash__()
            else:
                self.is_valid = False
                self.colors['passwd_color'] = MForm.SOLIDAREITCOLOR
                self.colors['passwdC_color'] = MForm.SOLIDAREITCOLOR
            
            ### ADDRESS ##
            if form['street'] != ''and match(r"^[a-zA-Z0-9 ]*$", form['name']):
                self.street = form['street']
            else:
                self.is_valid = False
                self.colors['street_color'] = MForm.SOLIDAREITCOLOR
            
            if form['streetnumber'] != '' and match(r"^[0-9]{1,5}$", form['streetnumber']):
                self.streetnumber = form['streetnumber']
            else:
                self.is_valid = False
                self.colors['streetnumber_color'] = MForm.SOLIDAREITCOLOR
    
            if form['city'] != '':
                self.city = form['city']
            else:
                self.is_valid = False
                self.colors['city_color'] = MForm.SOLIDAREITCOLOR
                
            if form['postcode'] != '' and match(r"^[0-9]{1,9}$", form['postcode']):
                self.postcode = form['postcode']
            else:
                self.is_valid = False
                self.colors['postcode_color'] = MForm.SOLIDAREITCOLOR
                
            self.phone = form['phone']
            self.id_card = form['id_card']
            self.facebook = form['facebook']
            
    def is_valid(self):
        print(self.is_valid)
        return self.is_valid