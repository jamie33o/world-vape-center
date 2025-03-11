"""
URL patterns for the profile application.

This module defines the URL patterns and
routing configuration for the
application. Each URL pattern is associated
with a specific view function or
class, determining the mapping between URLs
and the corresponding
presentation logic.

"""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('shipping/',
         views.shipping_address_view,
         name='shipping_address_view'),
    path('favourites/', views.favourites_view, name='favourites'),

    path('orders/', views.orders_view, name='profile_orders'),
    path('tickets/', views.tickets_view, name='profile_tickets'),

    path('sign_in/', views.signin_view, name='sign_in'),
    path('sign_up/', views.signup_view, name='sign_up'),
]
