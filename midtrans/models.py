from .utils import random_order_id
from django.db.models.signals import pre_save
from django.db import models
import datetime
from django.contrib import admin

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=1)
    stock = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = (self.price * self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

ORDER_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
)

class Order(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    order_id = models.CharField(max_length=255, default=random_order_id, unique=True)
    order_date = models.DateTimeField(default=datetime.datetime.now)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=255, default='pending')
    price = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = (self.price * self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.product_name} [Quantity: {self.quantity}] [Order ID: {self.order_id}]"

def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = random_order_id()

pre_save.connect(pre_save_order_id, sender=Order)

class CheckoutData(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True) 
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=255, default=random_order_id, unique=True)
    order_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Checkout Data for Order ID: {self.order_id}"

class SearchOrderId(admin.ModelAdmin):
    search_fields = ['order_id', 'product_name']