from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adres-wysylki/', views.OrderCreateView.as_view(), name='order_create_view'),
    url(r'^potwierdzenie/', views.OrderConfirmView.as_view(), name='order_confirm_view'),
]