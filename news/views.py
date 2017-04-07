from django.shortcuts import render
from django.views.generic import View
from django.contrib. messages.views import SuccessMessageMixin

from .forms import JoinForm
from products.models import Category

class HomeView(View):
    form = JoinForm
    template = 'news/home.html'
    

    def get(self, request):
        form = self.form(None)
        categories = Category.objects.all()
        context = {
            'form':form,
            'categories': categories
        }
        return render(request, self.template, context)
        
    def post(self, request):
        categories = Category.objects.all()
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            form = self.form()
        
        context = {
            'form':form,
            'categories': categories
        }
        return render(request, self.template, context)