from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from products.models import Category, Product

from. models import Join, Faq
from .forms import JoinForm, ContactForm


class HomeView(View):
    form = JoinForm
    template = 'news/home.html'

    def get(self, request):
        new_products = Product.active_objects.filter(is_new=True)
        context = {
            'products': new_products,
        }
        return render(request, self.template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            messages.success(request, 'Dziękujemy! Zapisaliśmy Twój e-mail.', extra_tags='newsletter')
            form = self.form()
        else:
            messages.error(request, 'Podany e-mail jest już w naszej bazie!', extra_tags='newsletter')

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
        contact_form = self.form(None)
        context = {
            'contact_form': contact_form
        }
        return render(request, self.template, context)
        
    def post(self, request):
        contact_form = self.form(request.POST)
        if contact_form.is_valid():
            first_name = contact_form.cleaned_data.get("first_name")
            last_name = contact_form.cleaned_data.get("last_name")
            subject = contact_form.cleaned_data.get("subject")
            email = contact_form.cleaned_data.get("email")
            message = contact_form.cleaned_data.get("message")
            contact_message = "{} {} via {}: {}".format(first_name, last_name, email, message)
            from_mail = settings.EMAIL_HOST_USER
            to_mail = ['dworanowski.adrian@gmail.com']
            
            send_mail(subject, contact_message, from_mail, to_mail, fail_silently=False)
            
            contact_form = self.form(None)
            messages.success(request, 'Wiadomość została wysłana. Dziękujemy!', extra_tags='contact-form')
            
        context = {
            'contact_form': contact_form
        }
        return render(request, self.template, context)


class AboutView(View):
    def get(self, request):
        template = 'news/about.html'
        context = {}
        return render(request, template, context)
        
        
class CustomOrdersView(View):
    def get(self, request):
        template = 'news/custom-orders.html'
        context = {}
        return render(request, template, context)


class NotFoundView(View):
    def get(self, request):
        template = '404.html'
        context = {}
        return render(request, template, context)
