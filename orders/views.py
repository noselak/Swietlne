from django.shortcuts import render
from django.views.generic import View

from .models import OrderItem
from .forms import OrderCreateForm
from users.models import UserProfile
from cart.cart import Cart


class OrderCreateView(View):

    def get(self, request):
        template = 'orders/order_create.html'
        order_create_form = OrderCreateForm()
        # prepopulate form for logged users
        if request.user.is_authenticated():
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            email = user.email
            full_name = user_profile.full_name
            address = user_profile.address
            phone = user_profile.phone
            data = {
                'email': email,
                'full_name': full_name,
                'address': address,
                'phone': phone
            }
            order_create_form = OrderCreateForm(initial=data)
        context = {
            'order_create_form': order_create_form
        }
        return render(request, template, context)

    def post(self, request):
        template = 'orders/order_accept.html'
        cart = Cart(request)
        order_create_form = OrderCreateForm(request.POST)
        if order_create_form.is_valid():
            order = order_create_form.save(commit=False)
            if request.user.is_authenticated():
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            context = {
                'order': order
            }
            return render(request, template, context)


class OrderConfirmView(View):
    template = 'orders/order_confirm.html'
    
    def post(self, request):
        pass