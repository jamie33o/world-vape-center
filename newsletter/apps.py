from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    """
    Newsletter Configuration

    Configures the 'newsletter' app for integration with the Django project.

    Attributes:
        default_auto_field (str): The default auto field for model primary keys.
        name (str): The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'
