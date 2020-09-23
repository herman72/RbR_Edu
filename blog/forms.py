from django import forms
from django.forms import HiddenInput

from blog.models import Post, Comment, UserBlog
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        euser = self.cleaned_data['email']
        try:
            UserBlog.objects.get(email=euser)
            return euser
        except:
            raise ValidationError("There is no email in database!")


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserBlog
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ChangePassForm(forms.Form):
    password11 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    password22 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

    email = forms.EmailField(max_length=255, widget=forms.HiddenInput())
    code = forms.CharField(max_length=32, widget=forms.HiddenInput())

    def clean_password22(self):

        if self.cleaned_data['password11'] != self.cleaned_data['password22']:
            print('i am here')
            # self.add_error(field='password22', error=ValidationError("no same pass"))
            raise ValidationError("no same pass")
        else:
            return self.cleaned_data['password11']


