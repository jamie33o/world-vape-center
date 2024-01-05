from django.contrib import admin
from .models import Product, Brand, Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)