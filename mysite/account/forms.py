from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    #password = forms.CharField(widget=forms.PasswordInput)


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
    
#allows users to edit their firt and last name and email which are attributes of django user model
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']

#allow users to edit the profile data
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']