from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'address', 'phone')
        labels = {
            'full_name': 'Imię i nazwisko',
            'email': 'E-mail',
            'address': 'Adres do wysyłki',
            'phone': 'Telefon'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }