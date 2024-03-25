from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """
    Model representing a support ticket.
    """

    TITLE_CHOICES = [
        ("question", "Question"),
        ("site_error", "Site Error"),
        ("order_issue", "Order Issue"),
        ("delivery_issue", "Delivery Issue"),
        ("refund_request", "Refund Request"),
        ("account_issue", "Account Issue"),
        ("feedback", "Feedback"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=20, choices=TITLE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Ticket object.
        """
        return dict(self.TITLE_CHOICES)[self.title]


class TicketMessages(models.Model):
    """
    Model representing a message associated with a ticket.
    """

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="ticket_messages"
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the TicketMessage object.
        """
        return f"Message from {self.sender} on {self.created_at}"
