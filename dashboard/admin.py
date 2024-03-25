from django.contrib import admin
from .models import Ticket, TicketMessages

admin.site.register(Ticket)
admin.site.register(TicketMessages)