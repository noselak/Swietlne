from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    url(r'^logowanie/$', views.LoginView.as_view(), name='login'),
    url(r'^rejestracja/$', views.RegisterView.as_view(), name='register'),
    url(r"^wyloguj/$", auth_views.logout_then_login, name="logout"),
    url(r'^profil/$', views.ProfileView.as_view(), name='profile'),
    url(r'^lista-zyczen/', views.WishlistView.as_view(), name='wishlist'),
    url(r'^haslo/', views.PasswordChangeView.as_view(), name='password_change'),
]