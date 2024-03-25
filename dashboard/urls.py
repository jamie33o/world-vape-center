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
    orders_dashboard,
    orders,
    change_order_status,
    overview_dashboard,
    tickets_dashboard,
    tickets,
    change_ticket_status,
    open_ticket,
    ticket_response,
)

urlpatterns = [
    path("orders", orders_dashboard, name="orders"),
    path("orders/<str:status>", orders, name="orders_list"),
    path("change_status/<int:order_id>", change_order_status, name="change_status"),
    path("overview", overview_dashboard, name="overview"),
    path("tickets", tickets_dashboard, name="tickets"),
    path("tickets/<str:title>", tickets, name="ticket"),
    path(
        "change_ticket_status/<int:ticket_id>",
        change_ticket_status,
        name="change_ticket_status",
    ),
    path("open_ticket/", open_ticket, name="open_ticket"),
    path("ticket_response/<int:ticket_id>", ticket_response, name="ticket_response"),
]
