"""
URL patterns for the dashboard application.

This module defines the URL patterns and
routing configuration for the
application. Each URL pattern is associated
with a specific view function or
class, determining the mapping between URLs
and the corresponding
presentation logic.

"""

from django.urls import path
from .views import (
    open_ticket,
    ticket_response,
)

urlpatterns = [
    path("open_ticket/", open_ticket, name="open_ticket"),
    path("ticket_response/<int:ticket_id>",
         ticket_response, name="ticket_response"),
]
