from decimal import Decimal
from django.contrib import admin

@admin.action(description="Apply 5%% discount to selected products")
def apply_five_percentage_discount(modeladmin, request, queryset):
    # Update the 'discount' field for selected products
    for product in queryset:
        five_percent = Decimal(0.05) * Decimal(product.price)
        product.discounted_price = product.price - five_percent
        product.discount_percentage = '5% OFF'
        product.save()


@admin.action(description="Apply 10%% discount to selected products")
def apply_ten_percentage_discount(modeladmin, request, queryset):
    # Update the 'discount' field for selected products
    for product in queryset:
        ten_percent = Decimal(0.10) * Decimal(product.price)
        product.discounted_price = product.price - ten_percent
        product.discount_percentage = '10% OFF'
        product.save()

@admin.action(description="Apply 20%% discount to selected products")
def apply_twenty_percentage_discount(modeladmin, request, queryset):
    # Update the 'discount' field for selected products
    for product in queryset:
        twenty_percent = Decimal(0.20) * Decimal(product.price)
        product.discounted_price = product.price - twenty_percent
        product.discount_percentage = '20% OFF'
        product.save()

@admin.action(description='Apply 50%% discount to selected products')
def apply_fifty_percentage_discount(modeladmin, request, queryset):
    # Update the 'discount' field for selected products
    for product in queryset:
        fifty_percent = Decimal(0.50) * Decimal(product.price)
        product.discounted_price = product.price - fifty_percent
        product.discount_percentage = '50% OFF'
        product.save()

@admin.action(description='Remove discount')
def remove_discount(modeladmin, request, queryset):
    # Update the 'discount' field for selected products
    for product in queryset:
        product.discounted_price = 0
        product.discount_percentage = ''
        product.save()