from django.contrib import admin
from .models import Ticket, Ticket_messages

admin.site.register(Ticket)
admin.site.register(Ticket_messages)