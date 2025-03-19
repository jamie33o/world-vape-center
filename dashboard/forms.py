from django import forms
from .models import Ticket, TicketMessages

class TicketForm(forms.ModelForm):
    """
    Form for creating a new ticket.
    """

    class Meta:
        model = Ticket
        fields = ["title", "description"]
        widgets = {
            "title": forms.Select(choices=Ticket.TITLE_CHOICES),
        }


class TicketResponseForm(forms.ModelForm):
    """
    Form for responding to a ticket.
    """

    class Meta:
        model = TicketMessages
        fields = ["message"]
