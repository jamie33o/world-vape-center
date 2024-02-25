"""
Help Config

Django application configuration for the 'help' app.

Attributes:
    default_auto_field (str): The default auto-generated field for models.
    name (str): The name of the 'help' app.
"""
from django.apps import AppConfig

class HelpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'help'
