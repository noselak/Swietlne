"""swietlny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from news.views import NotFoundView

urlpatterns = [
    url(r'', include('news.urls', namespace="news")),
    url(r'^produkty/', include('products.urls', namespace="products")),
    url(r'^uzytkownicy/', include('users.urls', namespace="users")),
    url(r'^koszyk/', include('cart.urls', namespace="cart")),
    url(r'^zamowienia/', include('orders.urls', namespace="orders")),
    url(r'^admin/', admin.site.urls),
]

handler404 = NotFoundView.as_view()

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
