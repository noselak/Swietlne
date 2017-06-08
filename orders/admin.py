from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "created", "status", "accepted"]
    search_fields = ["pk", "user"]
    list_filter = ["created"]
    inlines = [OrderItemInline]
    
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
