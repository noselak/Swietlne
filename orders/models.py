from django.db import models
from django.contrib.auth.models import User

from products.models import Product

STATUS_CHOICES = (
                    ('awaiting', 'Oczekuje na płatność'),
                    ('in_progress', 'W przygotowaniu'),
                    ('sent', 'Wysłano'),
                    ('cancelled', 'Anulowano')
    )
    
class AcceptedOrderManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        super(AcceptedOrderManager, self).get_queryset().filter(
            accepted=True)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=70)
    email = models.EmailField()
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=70, 
            default='awaiting')
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=10.00)
    
    accepted_orders = AcceptedOrderManager()
    
    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'
    
    def __str__(self):
        return "Order #{}, ".format(self.pk)
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.shipping_total_price
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
            related_name='items')
    product = models.ForeignKey(Product, related_name="order_items")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return "Order Item #{}, ".format(self.pk)
    
    def get_cost(self):
        return self.price * self.quantity