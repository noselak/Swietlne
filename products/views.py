from django.shortcuts import render
from django.views.generic import View

from .models import Product, Category


class CategoryView(View):
    template = 'products/category.html'
    
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(categories=category)
        context = {
            'products': products,
        }
        return render(request, self.template, context)
