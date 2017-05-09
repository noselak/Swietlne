from django.shortcuts import render
from django.views.generic import View
from django.core.mail import send_mail
from django.conf import settings

from .models import Order, OrderItem
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
        cart = Cart(request)
        order_create_form = OrderCreateForm(request.POST)
        if order_create_form.is_valid():
            template = 'orders/order_accept.html'
            order = order_create_form.save(commit=False)
            if request.user.is_authenticated():
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            context = {
                'order': order
            }
            return render(request, template, context)

        template = 'orders/order_create.html'
        order_create_form = OrderCreateForm()
        context = {
            'order_create_form': order_create_form
        }
        return render(request, template, context)


class OrderConfirmView(View):
    template = 'orders/order_confirm.html'

    def post(self, request):
        cart = Cart(request)
        order_pk = request.POST.get('order_pk')
        order = Order.objects.get(pk=order_pk)
        order.accepted = True
        order.save()
        cart.clear()

        # Sending e-mail notification to the client and admin
        full_name = order.full_name
        subject = "Potwierdzenie złożenia zamówienia nr {}".format(order.pk)
        email = order.email
        order_items = order.items.all()
        message = """Dziękujemy za złożenie zamówienia. 
                    Zamówione przedmioty: \n"""
        for item in order_items:
            message += "{}: Ilość: {}\n".format(item.product.title, item.quantity)
        contact_message = "{} via {}: \n{}".format(full_name, email, message)
        from_mail = settings.EMAIL_HOST_USER
        to_mail = [settings.EMAIL_HOST_USER, order.email]
        send_mail(subject, contact_message, from_mail, to_mail, fail_silently=False)

        context = {
            'order': order
        }
        return render(request, self.template, context)
