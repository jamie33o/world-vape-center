from django.contrib import admin
from .models import Order, OrderLineItem, ShippingAddress

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderLineItem)
admin.site.register(ShippingAddress)