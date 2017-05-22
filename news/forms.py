from django import forms

from .models import Join

class JoinForm(forms.ModelForm):
    email = forms.EmailField(label='', 
            widget=forms.EmailInput(
                attrs={
                    'placeholder': 'Twój e-mail',
                    'class': 'form-control',
                    'id': 'newsletter-email'
                }))
    class Meta:
        model = Join
        fields = ['email']
        
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        qs = Join.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Podany e-mail jest już w naszej bazie.")
        return email

   
class ContactForm(forms.Form):
    first_name = forms.CharField(
                                required=False, 
                                label="Imię", 
                                widget=forms.TextInput(attrs={
                                                            'class': "form-control",
                                                            'id': 'contact-first-name'
                                                            }
                                                    )
                                )
    last_name = forms.CharField(
                                required=False, 
                                label="Nazwisko", 
                                widget=forms.TextInput(attrs={
                                                            'class': "form-control",
                                                            'id': 'contact-last-name'
                                                            }
                                                    )
                                )
    subject = forms.CharField(
                            label="Temat", 
                            widget=forms.TextInput(attrs={
                                                        'class': "form-control",
                                                        'id': 'contact-subject'
                                                        }
                                                )
                            )
    email = forms.EmailField(
                            label="E-mail", 
                            widget=forms.TextInput(attrs={
                                                        'class': "form-control",
                                                        'id': 'contact-email'
                                                        }
                                                )
                            )
    message = forms.CharField(
                            label="Wiadomość", 
                            widget=forms.Textarea(attrs={
                                                        'class': "form-control",
                                                        'id': 'contact-message'
                                                        }
                                                )
                            )