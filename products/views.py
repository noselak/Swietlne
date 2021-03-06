from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from cart.forms import CartUpdateProductForm
from comments.forms import CommentCreateForm
from comments.models import Comment

from .models import Product, Category


class CategoryView(View):
    template = 'products/category.html'
    
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.active_objects.filter(categories=category)
        
        try:
            request.session['num_filter'] = request.GET['num']
            request.session['sort_by'] = request.GET['sort_by']
        except:
            pass
        
        num_filter = request.session.get('num_filter') or 9
        sort_by = request.session.get('sort_by') or 'title'
        
        cart_form = CartUpdateProductForm()
        
        paginator = Paginator(products, num_filter)
        page = request.GET.get('page')
        
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
            'cart_form': cart_form
        }
        return render(request, self.template, context)


class ProductView(View):
    template = 'products/product.html'
    
    def get(self, request, pk):
        product = Product.active_objects.get(pk=pk)
        cart_form = CartUpdateProductForm()
        comments = product.comments().filter(comment_parent=None)
        data = {
            'content_type': product.content_type,
            'object_id': product.pk,
        }
        comment_create_form = CommentCreateForm(None, initial=data)
        context = {
            'product': product,
            'comments': comments,
            'cart_form': cart_form,
            'comment_create_form': comment_create_form
        }
        return render(request, self.template, context)
        
    def post(self, request, pk):
        comment_create_form = CommentCreateForm(request.POST)
        print(comment_create_form)
        
        if comment_create_form.is_valid():
            comment_username = comment_create_form.cleaned_data.get('comment_username')
            comment_body = comment_create_form.cleaned_data.get('comment_body')
            c_type = comment_create_form.cleaned_data.get('content_type').lower()
            content_type = ContentType.objects.get(model=c_type)
            object_id = comment_create_form.cleaned_data.get('object_id')
            comment_parent = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                comment_parent = Comment.objects.get(pk=parent_id)
            new_comment = Comment.objects.create(
                comment_username=comment_username,
                comment_body=comment_body,
                comment_parent=comment_parent,
                content_type=content_type,
                object_id=object_id
                )
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        return redirect('news:home')

        
class SearchView(View):
    template = 'products/search.html'

    def get(self, request):
        query = request.GET.get('q')
        
        try:
            request.session['num_filter'] = request.GET['num']
            request.session['sort_by'] = request.GET['sort_by']
        except:
            pass
        
        num_filter = request.session.get('num_filter') or 9
        sort_by = request.session.get('sort_by') or 'title'
        
        cart_form = CartUpdateProductForm()
        if query:
            products_all = Product.active_objects.filter(
                                                        Q(title__icontains=query) | 
                                                        Q(description__icontains=query)
                                                        ).distinct()
        else:
            # display only most populars products if there's no query
            products_all = Product.active_objects.filter(best_buy=True)

        paginator = Paginator(products_all, num_filter)
        page = request.GET.get('page')    

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
            'cart_form': cart_form
        }
        return render(request, self.template, context)
