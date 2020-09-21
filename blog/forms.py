from django import forms
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
            q = UserBlog.objects.get(email=euser)
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
    password1 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

    def clean_pass(self):

        if not self.password1 == self.password2:

            raise ValidationError("no same pass")
