from decimal import Decimal
from django.contrib import admin


def apply_discount_to_products(queryset, discount_percent):
    """
    Apply a percentage discount to the selected products.

    Args:
        queryset (QuerySet): The queryset containing the selected products.
        discount_percent (int): The percentage discount to be applied.

    Returns:
        None
    """
    for product in queryset:
        discount_amount = Decimal(discount_percent) * Decimal(product.price)
        product.discounted_price = product.price - discount_amount
        product.discount_percentage = f'{discount_percent}% OFF'
        product.save()


@admin.action(description="Apply 5%% discount to selected products")
def apply_five_percentage_discount(modeladmin, request, queryset):
    """
    Admin action to apply a 5% discount to selected products.
    """
    apply_discount_to_products(queryset, 5)


@admin.action(description="Apply 10%% discount to selected products")
def apply_ten_percentage_discount(modeladmin, request, queryset):
    """
    Admin action to apply a 10% discount to selected products.
    """
    apply_discount_to_products(queryset, 10)


@admin.action(description="Apply 20%% discount to selected products")
def apply_twenty_percentage_discount(modeladmin, request, queryset):
    """
    Admin action to apply a 20% discount to selected products.
    """
    apply_discount_to_products(queryset, 20)


@admin.action(description="Apply 50%% discount to selected products")
def apply_fifty_percentage_discount(modeladmin, request, queryset):
    """
    Admin action to apply a 50% discount to selected products.
    """
    apply_discount_to_products(queryset, 50)


@admin.action(description="Remove discount")
def remove_discount(modeladmin, request, queryset):
    """
    Admin action to remove the discount from selected products.
    """
    for product in queryset:
        product.discounted_price = 0
        product.discount_percentage = ''
        product.save()
