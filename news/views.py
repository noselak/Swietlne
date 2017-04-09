from django.shortcuts import render
from django.views.generic import View

from .forms import JoinForm
from products.models import Category, Product

class HomeView(View):
    form = JoinForm
    template = 'news/home.html'

    def get(self, request):
        form = self.form(None)
        best_buy_products = Product.active_objects.filter(best_buy=True)
        context = {
            'form':form,
            'products': best_buy_products,
        }
        return render(request, self.template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        best_buy_products = Product.active_objects.filter(best_buy=True)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            form = self.form()
        
        context = {
            'form':form,
            'products': best_buy_products,
        }
        return render(request, self.template, context)