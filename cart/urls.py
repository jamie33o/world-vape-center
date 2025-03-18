"""
Module: urls.py
Django URL patterns for the cart app.

This module defines the URL patterns for various cart-related views,
including adding, deleting, updating, and displaying the cart summary.
"""

from django.urls import path
from .views import cart_add, cart_delete, cart_summary, cart_update

urlpatterns = [
    path('', cart_summary, name='cart-summary'),
    path('add/<int:product_id>/', cart_add, name='cart-add'),
    path('delete/<str:sku>/', cart_delete, name='cart-delete'),
    path('update/<str:sku>/', cart_update, name='cart-update'),
]
