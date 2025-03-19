
from django.shortcuts import redirect
from django.contrib import messages
from .models import Ticket
from .forms import (
                    TicketForm,
                    TicketResponseForm)

def open_ticket(request):
    """
    Open a new ticket.

    Returns:
        HttpResponse: Redirects to a specified URL.
    """
    ticket_form = TicketForm(request.POST)
    url = request.POST.get("url")
    if ticket_form.is_valid():
        ticket_form.instance.user = request.user
        ticket_form.save()
        messages.success(request, "Ticket opened")
    else:
        messages.error(request, ticket_form.errors)
    return redirect(url)


def ticket_response(request, ticket_id):
    """
    Respond to a ticket.

    Returns:
        HttpResponse: Redirects to a specified URL.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    ticket_response_form = TicketResponseForm(request.POST)
    url = request.POST.get("url")
    if ticket_response_form.is_valid():
        ticket_message = ticket_response_form.save(commit=False)
        ticket_message.sender = request.user
        ticket_message.ticket = ticket
        ticket_message.save()
        messages.success(request, "Response sent")
    else:
        messages.error(request, ticket_response_form.errors)
    return redirect(url)
