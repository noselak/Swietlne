from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Product
from orders.models import Order
from cart.forms import CartUpdateProductForm

from .forms import LoginForm, UserForm, UserProfileForm, PasswordChangeCustomForm
from .models import UserProfile


class RegisterView(View):
    template = 'users/register.html'
    
    def get(self, request):
        user_form = UserForm()
        user_profile_form = UserProfileForm()
        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form
        }
        return render(request, self.template, context)
        
    def post(self, request):
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Utworzono nowe konto!', 
                                extra_tags='register')
            
            user_form = UserForm()
            user_profile_form = UserProfileForm()
        
        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form
        }
        return render(request, self.template, context)


class LoginView(View):
    template = 'users/register.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if '@' in username:
            try:
                username = User.objects.get(email=username)
            except:
                pass
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 
                            'Użytkownik {} został zablokowany'.format(username), 
                            extra_tags='login')
                return redirect('users:register')
        else:
            messages.error(request, 'Błędne hasło i/lub nazwa użytkownika', 
                            extra_tags='login')
            return redirect('users:register')
        
    def get(self, request, *args, **kwargs):
        return redirect('users:register')


class ProfileView(View):
    template = 'users/account.html'
    
    @method_decorator(login_required(login_url='users:register'))
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        user_profile = UserProfile.objects.get(user=user)
        data = {
            'full_name': user_profile.full_name, 
            'address': user_profile.address,
            'phone': user_profile.phone,
        }
        user_profile_form = UserProfileForm(None, initial=data)
        user_password_form = PasswordChangeCustomForm(None)
        
        context = {
            'user_profile_form': user_profile_form,
            'user_password_form': user_password_form
        }
        return render(request, self.template, context)
        
    @method_decorator(login_required(login_url='users:register'))    
    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        user_profile = UserProfile.objects.get(user=user)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            print(user_profile.address)
            user_profile.save()
        return redirect('users:profile')


class PasswordChangeView(View):
    template = 'users/account.html'
    
    def get(self, request):
        return redirect('users:profile')
    
    @method_decorator(login_required(login_url='users:register')) 
    def post(self, request):
        user_password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if user_password_form.is_valid():
            user = user_password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Zmiana hasła się powiodła!', 
                            extra_tags='password')
            return redirect('users:profile')
        else:
            messages.error(request, 
                            'Zmiana hasła się nie powiodła! Spróbuj ponownie', 
                            extra_tags='password')
                            
        user = User.objects.get(pk=request.user.pk)
        user_profile = UserProfile.objects.get(user=user)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        
        context = {
            'user_profile_form': user_profile_form,
            'user_password_form': user_password_form
        }
        return render(request, self.template, context)


class WishlistView(View):
    template = 'users/wishlist.html'
    
    @method_decorator(login_required(login_url='users:register'))
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        products = Product.objects.filter(wishlist=user)
        cart_form = CartUpdateProductForm()
        context = {
            'products': products,
            'cart_form': cart_form
        }
        return render(request, self.template, context)
        
    @method_decorator(login_required(login_url='users:register'))
    def post(self, request):
        product_pk = request.POST.get("wishlist") or request.POST.get("remove_wishlist")
        user = User.objects.get(pk=request.user.pk)
        product = Product.objects.get(pk=product_pk)
        if request.POST.get("wishlist") is not None:
            if product not in Product.objects.filter(wishlist=user):
                product.wishlist.add(user)
                product.save()
                messages.success(request, 'Produkt {} dodany do listy życzeń!'.format(product), 
                                extra_tags='wishlist')
            else:
                messages.error(request, 'Produkt {} już jest na Twojej liście życzeń!'.format(product), 
                                extra_tags='wishlist')
        elif request.POST.get("remove_wishlist") is not None:
            if product in Product.objects.filter(wishlist=user):
                product.wishlist.remove(user)
                product.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderListView(View):
    template = 'users/orders.html'

    @method_decorator(login_required(login_url='users:register'))
    def get(self, request):
        user = request.user
        orders = Order.accepted_orders.filter(user=user)
        
        context = {
            'orders': orders
        }
        return render(request, self.template, context)


class OrderView(View):
    template = 'users/order_detail.html'
    
    @method_decorator(login_required(login_url='users:register'))
    def get(self, request, pk):
        order =  get_object_or_404(Order, pk=pk)
        if order.user == request.user:
            context = {
                'order': order
            }
            return render(request, self.template, context)
        else:
            return redirect('users:profile')
