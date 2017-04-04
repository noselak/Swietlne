from django.shortcuts import render
from django.views.generic import View

class HomeView(View):
    def get(self, request):
        template = 'news/home.html'
        context = {}
        return render(request, template, context)
