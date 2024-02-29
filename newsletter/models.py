from django.db import models

class Subscriber(models.Model):
    """
    Subscriber Model

    Represents a subscriber to the newsletter.

    Attributes:
        email (EmailField): The unique
        email address of the subscriber.
        subscribed_at (DateTimeField):
        The date and time when the subscriber subscribed.

    """
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
