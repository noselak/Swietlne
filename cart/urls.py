from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.CartView.as_view(), name="cart_view"),
    url(r'^dodaj/(?P<pk>\d+)/$', views.AddToCartView.as_view(), name="add_to_cart_view"),
    url(r'^usun/(?P<pk>\d+)/$', views.RemoveFromCartView.as_view(), name="remove_from_cart_view"),
]