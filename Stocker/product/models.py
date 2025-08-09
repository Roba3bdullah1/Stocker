from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images/', blank=True, null=True, default='default.jpg')
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True, null=True, default='https://example.com')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
    ('available', 'Available'),      
    ('out_of_stock', 'Out of Stock'),
    ('discontinued', 'Discontinued'),
    ('low_stock', 'Low Stock'), 
]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    stock_quantity = models.PositiveIntegerField(default=0) 
    expiry_date = models.DateField(null=True, blank=True)

    LOW_STOCK_THRESHOLD = 5

    def is_low_stock(self):
        return 0 < self.stock_quantity < self.LOW_STOCK_THRESHOLD

    def is_out_of_stock(self):
        return self.stock_quantity == 0

    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False