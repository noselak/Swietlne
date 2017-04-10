from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category


class CategoryView(View):
    template = 'products/category.html'
    
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.active_objects.filter(categories=category)
        num_filter = request.GET.get('num') or 9
        sort_by = request.GET.get('sort_by') or 'title'
        
        paginator = Paginator(products, num_filter)
        page = request.GET.get('page')
        
        display_count = category.products_count - ((paginator.num_pages-1) * int(num_filter))
        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        
        context = {
            'products': products,
            'category': category,
            'sort_by': sort_by,
            'num_filter': num_filter,
            'display_count': display_count,
        }
        return render(request, self.template, context)
