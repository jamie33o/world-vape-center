from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket, TicketMessages

@receiver(post_save, sender=Ticket)
def send_ticket_opened_email(sender, instance, created, **kwargs):
    if created:
        subject = "A new ticket has been opened"
        message = f"Details:\nTitle: {instance.title}\nCreated at: {instance.created_at}"
        recipient_list = [settings.EMAIL_HOST_USER]
        if instance.user:
            recipient_list.append(instance.user.email)
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_save, sender=TicketMessages)
def send_ticket_message_email(sender, instance, created, **kwargs):
    if created:
        ticket = instance.ticket
        subject = f"A new message has been added to the ticket '{ticket.title}'"
        message = f"Ticket Details:\nTitle: {ticket.title}\nMessage: \
            {instance.message}\nCreated at: {instance.created_at}\
                \nSender: {instance.sender if not instance.sender.is_staff else 'Admin'}"
        recipient_list = [settings.EMAIL_HOST_USER]
        if instance.user:
            recipient_list.append(instance.user.email)
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
