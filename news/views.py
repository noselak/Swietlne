from django.shortcuts import render
from django.views.generic import View

from .forms import JoinForm

class HomeView(View):
    form = JoinForm

    def get(self, request):
        form = self.form(None)
        template = 'news/home.html'
        context = {
            'form':form
        }
        return render(request, template, context)
        
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            email = form.cleaned_data.get('email')
            instance.email = email
            instance.save()
            form = self.form()
        
        template = 'news/home.html'
        context = {
            'form':form
        }
        return render(request, template, context)