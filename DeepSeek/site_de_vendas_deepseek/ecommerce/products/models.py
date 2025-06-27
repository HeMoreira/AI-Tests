from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    
    unique_id = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    date_added = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_priority_display(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, '')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.name}"