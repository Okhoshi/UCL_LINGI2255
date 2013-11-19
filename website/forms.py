from django import forms
from website.exceptions import *


class MForm(forms.Form):
    #Static variables
    ORG = True
    IND = False

    def __init__(self, request):
        form = request.POST

        if form.__contains__('organisation'):
            self.type = mForm.ORG
        else:
            self.type = mForm.IND

        if is_valid(self, request):
            self.name = form['name']
            self.first_name = form['first_name']
            self.user_name = form['user_name']
            self.email = form['email']
            if form['passwd'] == form['passwdC']:
                self.passwd = form['passwd'].__hash__()
            else:
                raise WrongPasswdException()

            self.email = form['email']
    def is_valid(self, request):
        # TODO: validate the form
        return True