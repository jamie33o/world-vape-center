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
from .views import (ProfileView,
                    shipping_address_view,
                    signin_view,
                    signup_view)

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('shipping_address_view/',
         shipping_address_view,
         name='shipping_address_view'),
    path('sign_in/', signin_view, name='sign_in'),
    path('sign_up/', signup_view, name='sign_up'),
]
