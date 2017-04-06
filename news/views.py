from django.shortcuts import render
from django.views.generic import View
from django.contrib. messages.views import SuccessMessageMixin

from .forms import JoinForm

class HomeView(View):
    form = JoinForm
    template = 'news/home.html'

    def get(self, request):
        form = self.form(None)
        context = {
            'form':form
        }
        return render(request, self.template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            form = self.form()
        
        context = {
            'form':form
        }
        return render(request, self.template, context)