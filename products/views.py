from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Product, Category
from cart.forms import CartUpdateProductForm


class CategoryView(View):
    template = 'products/category.html'
    
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.active_objects.filter(categories=category)
        num_filter = request.GET.get('num') or 9
        sort_by = request.GET.get('sort_by') or 'title'
        cart_form = CartUpdateProductForm()
        
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
            'cart_form': cart_form
        }
        return render(request, self.template, context)
       
        
class ProductView(View):
    template = 'products/product.html'
    
    def get(self, request, pk):
        product = Product.active_objects.get(pk=pk)
        cart_form = CartUpdateProductForm()
        context = {
            'product': product,
            'cart_form': cart_form
        }
        return render(request, self.template, context)
    
        
class SearchView(View):
    template = 'products/search.html'
    
    def get(self, request):
        query = request.GET.get('q')
        num_filter = request.GET.get('num') or 9
        sort_by = request.GET.get('sort_by') or 'title'
        cart_form = CartUpdateProductForm()
        if query:
            products_all = Product.active_objects.filter(
                                                        Q(title__icontains=query) | 
                                                        Q(description__icontains=query)
                                                        ).distinct()
        else:
            # display only new product if there's no query
            products_all = Product.active_objects.filter(is_new=True)
        
        paginator = Paginator(products_all, num_filter)
        page = request.GET.get('page')    
        display_count = products_all.count() - ((paginator.num_pages-1) * int(num_filter))
        
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
            'products_all': products_all,
            'sort_by': sort_by,
            'num_filter': num_filter,
            'display_count': display_count,
            'cart_form': cart_form
        }
        return render(request, self.template, context)
