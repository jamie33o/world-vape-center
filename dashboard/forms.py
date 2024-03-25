from django import forms
from checkout.models import Order
from .models import Ticket, TicketMessages


class OrderStatusForm(forms.ModelForm):
    """
    Form for updating order status.
    """
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES)
        }


class TicketForm(forms.ModelForm):
    """
    Form for creating a new ticket.
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description']
        widgets = {
            'title': forms.Select(choices=Ticket.TITLE_CHOICES), 
        }


class TicketResponseForm(forms.ModelForm):
    """
    Form for responding to a ticket.
    """
    class Meta:
        model = TicketMessages
        fields = ['message']


class TicketStatusForm(forms.ModelForm):
    """
    Form for updating ticket status.
    """
    class Meta:
        model = Ticket
        fields = ['status']
        STATUS_CHOICES = [
            ('Open', 'Open'),
            ('Closed', 'Closed'),
        ]
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES)
        }
