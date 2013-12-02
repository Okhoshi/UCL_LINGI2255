from django import forms
from re import match
from django.contrib.auth.models import User


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
            self.errorlist['Name'] = 'Ce champ ne peut contenir que des lettres majuscules ou minuscules'

        ### FIRST NAME ###
        if form['first_name'] != '' and match(r"^[a-zA-Z ]*$", form['name']):
            self.first_name = form['first_name']
        else:
            self.is_valid = False
            self.colors['first_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['First name'] = 'Ce champ ne peut contenir que des lettres majuscules ou minuscules'

        ### USER NAME ###
        if form['user_name'] != '' and match(r"^.{3,15}$", form['user_name']):
            if User.objects.filter(username=form['user_name']).count() == 0:
                self.user_name = form['user_name']
            else:
                self.is_valid = False
                self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['User name'] = 'Ce username est deja utilise'
        else:
            self.is_valid = False
            self.colors['user_name_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['User name'] = 'Le username doit faire entre 3 et 15 caracteres'


        ### EMAIL ###
        if form['email'] != '' and match(r"[^@]+@[^@]+\.[^@]+", form['email']):
            self.email = form['email']
        else:
            self.is_valid = False
            self.colors['email_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Email'] = 'Entrez un email valide'
            
        ### PASSWORD ###
        if form['passwd'] == form['passwdC'] and form['passwd'] != ''\
                and match(r"^[A-Za-z0-9,;:=?./+-_)(]{4,20}$", form['passwd']):
            self.passwd = form['passwd']
        else:
            self.is_valid = False
            self.colors['passwd_color'] = MForm.SOLIDAREITCOLOR
            self.colors['passwdC_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Password'] = 'Le mot de passe doit faire entre 4 et 20 characteres et ne peut contenit que des characteres alphanumeriqes ainsi que les symboles ",;:=?./+-_)("'
            
        ### ADDRESS ##
        if form['street'] != ''and match(r"^[a-zA-Z0-9 ]*$", form['name']):
            self.street = form['street']
        else:
            self.is_valid = False
            self.colors['street_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Street'] = 'La rue ne peut contenir que des characteres alphanumeriques'

        if form['streetnumber'] != '' and match(r"^[0-9]{1,5}$", form['streetnumber']):
            self.streetnumber = form['streetnumber']
        else:
            self.is_valid = False
            self.colors['streetnumber_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['Street number'] = 'Le numero de rue est un numero compose de 1 a 5 chiffres'
    
        if form['city'] != '' and match(r"^[a-zA-Z0-9 -_]*$", form['city']):
            self.city = form['city']
        else:
            self.is_valid = False
            self.colors['city_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['city'] = 'La ville ne peut contenir que des caracteres alphanumeriques ou les symboles "-_"'

                
        if form['country'] != '' and match(r"^[a-zA-Z0-9 -_]*$", form['country']):
            self.country = form['country']
        else:
            self.is_valid = False
            self.colors['country_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['country'] = 'Le pays ne peut contenir que des caracteres alphabetiques ou les symboles "-_"'
                
        if form['postcode'] != '' and match(r"^[0-9]{1,9}$", form['postcode']):
            self.postcode = form['postcode']
        else:
            self.is_valid = False
            self.colors['postcode_color'] = MForm.SOLIDAREITCOLOR
            self.errorlist['postcode'] = 'Le code postal est compose nombre de 1 a 9 chiffres'

        self.facebook = form['facebook']

        if form.__contains__('org_name'):
            self.type = MForm.ORG

            if form['org_name'] != '' and match(r"^[A-Za-z0-9,;:=?./+-_]*$", form['org_name']):
                self.org_name = form['org_name']
            else:
                self.is_valid = False
                self.colors['org_name_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['org_name'] = 'Le nom de l\'organisation...'
                
            
            if form['VAT'] == '' or match(r"^[A-Z0-9]*$", form['VAT']):
                self.VAT = form['VAT']
            else:
                self.is_valid = False
                self.colors['VAT_color'] = MForm.SOLIDAREITCOLOR
                self.errorlist['VAT'] = 'Le numero de TVA de l\'organisation...'
            
            self.org_site = form['org_site']
            self.org_phone = form['org_phone']
            self.description = form['description']
            
        else:
            self.type = MForm.IND
            self.phone = form['phone']
            self.id_card = form['id_card']
