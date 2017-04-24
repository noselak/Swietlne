from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^szukaj/', views.SearchView.as_view(), name='search_view'),
    url(r'^(?P<pk>\d+)/$', views.ProductView.as_view(), name="product_view"),
    url(r'^(?P<category_slug>[\w\-]+)/$', views.CategoryView.as_view(), name="category_view"),
    # url(r'^/$', views.Products.as_view(), name="products_view"),
]