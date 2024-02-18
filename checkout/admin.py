from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderLineItem)
