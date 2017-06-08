from django.contrib import admin

from .models import Category, Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "price", "active"]
    inlines = [ImageInline]
    
    class Meta:
        model = Product


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)