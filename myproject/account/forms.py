from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
    widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
    widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return data['password2']
    
    def clean_email(self):
        
        data = self.cleaned_data['email'].lower()

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    
    def clean_username(self):
        
        data = self.cleaned_data['username'].lower()

        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already in use.')
        return data

class AuthenticationFormWCaseInsensitive(AuthenticationForm):
    def clean_username(self):
        data = self.cleaned_data['username'].lower()
        return data        
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'email']

    def clean_usernam(self):
        data = self.cleaned_data['username'].lower()
        qs = User.objects.exclude(id=self.instance.id).filter(username=data)
        if qs.exists():
            raise forms.ValidationError('Username already in use.')
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
