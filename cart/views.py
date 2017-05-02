from django.shortcuts import render, redirect
from django.views.generic import View

from products.models import Product
from .cart import Cart
from .forms import CartUpdateProductForm



class AddToCartView(View):
    def post(self, request, pk):
        cart = Cart(request)
        product = Product.active_objects.get(pk=pk)
        cart_form = CartUpdateProductForm(request.POST)
        if cart_form.is_valid():
            cleaned_data = cart_form.cleaned_data
            print(cleaned_data['quantity'])
            cart.add(product=product,
                        quantity=cleaned_data['quantity'],
                        update_quantity=cleaned_data['update'])
        return redirect('cart:cart_view')
        
        
class RemoveFromCartView(View):
    def get(self, request, pk):
        cart = Cart(request)
        product = Product.active_objects.get(pk=pk)
        cart.remove(product)
        return redirect('cart:cart_view')
        

class CartView(View):
    template = 'cart/cart_detail.html'
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartUpdateProductForm(initial={
                'quantity': item['quantity'], 'update': True
            })
        context = {
            'cart': cart
        }
        return render(request, self.template, context)