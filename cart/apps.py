from django.apps import AppConfig

class CartConfig(AppConfig):
    """
    Configuration class for the 'cart' app.

    Attributes:
        default_auto_field (str): The default auto field for the app's models.
        name (str): The name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
