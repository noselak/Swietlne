from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Hasło", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'password', 'type': 'password'}))
                               
                               
class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    username = forms.CharField(label="Nazwa użytkownika", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'username'}))
    password1 = forms.CharField(label="Hasło", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'password1', 'type': 'password'}))
    password2 = forms.CharField(label="Potwierdź hasło", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'password2', 'type': 'password'}))
    email = forms.CharField(label="E-mail", max_length=30, 
                               widget=forms.TextInput(attrs=
                               {'class': 'form-control', 'name': 'email'}))
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('full_name', 'address', 'phone')
        labels = {
            'full_name': 'Imię i nazwisko',
            'address': 'Adres',
            'phone': 'Telefon'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
   
        
class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='Stare hasło', 
                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(required=True, label='Nowe hasło', 
                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(required=True, label='Potwierdź nowe hasło', 
                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    