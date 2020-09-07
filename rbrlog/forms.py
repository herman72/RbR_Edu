from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from mongoengine import DoesNotExist

from rbrlog.mongo_models import User


class LoginForm(forms.Form):

    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    user_name = forms.CharField(max_length=255, required=True)

    def clean_user_name(self):
        cuser = self.cleaned_data['user_name']

        try:
            q = User.objects.get(name=cuser)

        except DoesNotExist:

            raise ValidationError("There is no user with that name!")

        return cuser

    def clean(self):

        if 'user_name' in self.cleaned_data:
            cuser = self.cleaned_data['user_name']
            q = User.objects.get(name=cuser)

            if not check_password(self.cleaned_data['password'],q["hashed_password"]):
                raise ValidationError('Wrong Pass')

            return self.cleaned_data

class RegisterForm(forms.Form):

    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    user_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput)

    def clean_user_name(self):
        cuser = self.cleaned_data["user_name"]

        try:
            q = User.objects.get(name=cuser)

            print("why why why ???")

            raise ValidationError('same user name in database')

        except DoesNotExist:
            pass

        return cuser
