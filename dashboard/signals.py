from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket, TicketMessages

@receiver(post_save, sender=Ticket)
def send_ticket_opened_email(sender, instance, created, **kwargs):
    """
    Signal handler to send an email notification when a new ticket is opened.

    Parameters:
        sender (class): The class sending the signal (Ticket).
        instance (Ticket): The instance of Ticket being saved.
        created (bool): Indicates whether a new instance was created.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        subject = "World Vape Center... Ticket Notification"
        message = f"A new ticket has been opened\nDetails: {instance.description}\nTitle: {instance.title}\nCreated at: {instance.created_at}"
        recipient_list = [settings.EMAIL_HOST_USER]
        if instance.user:
            recipient_list.append(instance.user.email)
        from_email = settings.EMAIL_HOST_USER

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )

@receiver(post_save, sender=TicketMessages)
def send_ticket_message_email(sender, instance, created, **kwargs):
    """
    Signal handler to send an email notification when a new message is added to a ticket.

    Parameters:
        sender (class): The class sending the signal (TicketMessage).
        instance (TicketMessage): The instance of TicketMessage being saved.
        created (bool): Indicates whether a new instance was created.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        ticket = instance.ticket
        subject = "World Vape Center... Ticket Notification"
        message = f"A new message has been added to a ticket '{ticket.title}\n\
            Ticket Details:\nTitle: {ticket.title}\nMessage: \
            {instance.message}\nCreated at: {instance.created_at}\
                \nSender: {instance.sender if not instance.sender.is_staff else 'Admin'}"
        recipient_list = [settings.EMAIL_HOST_USER, ticket.user.email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )
