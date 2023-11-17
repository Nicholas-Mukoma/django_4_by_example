from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Repeat password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','email']

    def clean_password2(self):
         cd = self.cleaned_data
         if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
         return cd['password2']
    # prevents users form login in with an existing email address
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    
#allows users to edit their firt and last name and email which are attributes of django user model
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']
    # prevents user form changing their email address to an exisitin one
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)

        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

#allow users to edit the profile data
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']