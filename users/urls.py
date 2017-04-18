from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    url(r'^logowanie/$', auth_views.login, {'template_name': 'users/register.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^rejestracja/$', views.RegisterView.as_view(), name='register'),
    url(r"^wyloguj/$", auth_views.logout_then_login, name="logout"),
    # url(r'^profil/', views.ProfileView.as_view(), name='profile'),
]