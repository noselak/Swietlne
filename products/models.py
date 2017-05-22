from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment


# Category
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'
    
    def __str__(self):
        return self.title
    
    @property
    def products_count(self):
        products = Product.active_objects.filter(categories=self)
        return len(products)
        
        
# Product
class ActiveProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ActiveProductManager, self).get_queryset().filter(active=True)
  

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    best_buy = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User, blank=True)
    categories = models.ManyToManyField('Category')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    objects = models.Manager()
    active_objects =  ActiveProductManager()
    
    class Meta:
        ordering = ["title"]
        verbose_name = 'Product'
        verbose_name_plural = 'Produkty'
    
    def __str__(self):
        return self.title
    
    @property    
    def images(self):
        images = ProductImage.objects.filter(product=self)
        return images
    
    def get_absolute_url(self):
        return reverse('products:product_view', args=[str(self.pk)])
    
    @property  
    def content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type
        
    def comments(self):
        comments = Comment.objects.filter(object_id=self.pk)
        return comments


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    
    class Meta:
        verbose_name = 'Zdjęcie produktu'
        verbose_name_plural = 'Zdjęcia produktów'
    
    def __str__(self):
        return self.product.title
