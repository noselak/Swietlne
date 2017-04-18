from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, UserForm, UserProfileForm


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
