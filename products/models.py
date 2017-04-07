from django.db import models
from django.core.urlresolvers import reverse


# Category
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.title
        

class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).filter(active=True)
  
  
# Products
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    objects = ProductManager()
    
    class Meta:
        ordering = ["-title"]
    
    def __str__(self):
        return self.title
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    
    def __str__(self):
        return self.product.title
        

