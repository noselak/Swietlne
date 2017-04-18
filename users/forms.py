from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from django import forms

from .models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa użytkownika", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Hasło", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'type': 'password'}))
                               
                               
class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'E-mail',
            'password': 'Hasło'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}), 
        }
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('full_name', 'address', 'phone')
        labels = {
            'full_name': 'Imię i nazwisko',
            'address': 'Adres wysyłki',
            'phone': 'Telefon'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
        }
    