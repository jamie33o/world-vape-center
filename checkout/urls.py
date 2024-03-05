"""
Module for defining URL patterns in the checkout app.

This module includes URL patterns for
handling checkout-related views, success pages,
caching checkout data, and handling webhooks.

URL Patterns:
- '' (empty path): maps to views.checkout
- 'checkout_success/<order_number>':
maps to views.checkout_success
- 'cache_checkout_data/': maps to views.cache_checkout_data
- 'wh/': maps to the webhook view for handling webhooks
"""
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<int:order_id>',
         views.checkout_success,
         name='checkout_success'),
    path('cache_checkout_data/',
         views.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]
