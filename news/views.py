from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from. models import Join, Faq
from .forms import JoinForm, ContactForm
from products.models import Category, Product

class HomeView(View):
    form = JoinForm
    template = 'news/home.html'

    def get(self, request):
        best_buy_products = Product.active_objects.filter(best_buy=True)
        context = {
            'products': best_buy_products,
        }
        return render(request, self.template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            messages.success(request, 'Dziękujemy! Zapisaliśmy Twój e-mail.')
            form = self.form()
        else:
            messages.error(request, 'Podany e-mail jest już w naszej bazie!')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

class FaqView(View):
    template = 'news/faq.html'
    
    def get(self, request):
        faq = Faq.objects.all()
        context = {
            'faq': faq
        }
        return render(request, self.template, context)


class ContactView(View):
    form = ContactForm
    template = 'news/contact.html'
    
    def get(self, request):
        form = self.form(None)
        context = {
            'form': form
        }
        return render(request, self.template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            subject = form.cleaned_data.get("subject")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            contact_message = "{} {} via {}: {}".format(first_name, last_name, email, message)
            from_mail = settings.EMAIL_HOST_USER
            to_mail = ['dworanowski.adrian@gmail.com']
            
            send_mail(subject, contact_message, from_mail, to_mail, fail_silently=False)
            
            form = self.form(None)
            messages.success(request, 'Wiadomość została wysłana. Dziękujemy!')
            
        context = {
            'form': form
        }
        return render(request, self.template, context)