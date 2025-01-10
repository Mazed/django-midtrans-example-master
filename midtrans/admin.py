from django.contrib import admin
from .models import Product, Order, CheckoutData, SearchOrderId

admin.site.register(Product)
admin.site.register(Order, SearchOrderId)
admin.site.register(CheckoutData, SearchOrderId)