"""
Application configuration for the 'profile' app.

This module defines the configuration for the 'profile' app, specifying
customization options such as the default auto field and the app name.

Contents:
- AccountConfig: AppConfig class for the 'profile' app.

"""
from django.apps import AppConfig

class AccountConfig(AppConfig):
    """
    AppConfig class for the 'profile' app.

    Attributes:
    - default_auto_field (str): The default auto field for model creation.
    - name (str): The name of the 'profile' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile'
