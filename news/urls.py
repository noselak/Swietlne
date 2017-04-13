from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^kontakt/', views.ContactView.as_view(), name='contact'),
    url(r'^faq/', views.FaqView.as_view(), name='faq'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]