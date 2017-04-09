from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^(?P<pk>\d+)/$', views.ProductsDetail.as_view(), name="products_detail_view"),
    url(r'^(?P<category_slug>[\w\-]+)/$', views.CategoryView.as_view(), name="category_view"),
    # url(r'^/$', views.Products.as_view(), name="products_view"),
]