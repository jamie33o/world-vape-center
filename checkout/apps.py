"""
App configuration for the checkout app.

This AppConfig defines the configuration for the 'checkout' app in the Django project.
It specifies the default auto field and the name of the app.
"""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
