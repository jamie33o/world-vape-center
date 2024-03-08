"""
Module URLs Configuration for Help Pages

This module defines URL patterns for various help pages,
including payment options, delivery information,
about us, returns policy, terms, FAQ, contact us,
and the HTML sitemap.

Attributes:
    urlpatterns (list): List of URL patterns mapping to
    corresponding view functions.
"""
from django.urls import path
from .views import (payments_options, delivery_info,
                    about_us,
                    returns_policy,
                    terms,
                    faq,
                    contact_us,
                    sitemap_html,
                    privacy_policy
                    )

urlpatterns = [
    path('payments_options/', payments_options, name='payments_options'),
    path('delivery_info/', delivery_info, name='delivery_info'),
    path('about_us/', about_us, name='about_us'),
    path('returns_policy/', returns_policy, name='returns_policy'),
    path('terms/', terms, name='terms'),
    path('faq/', faq, name='faq'),
    path('contact-us.html/', contact_us, name='contact_us'),
    path('sitemap.html', sitemap_html, name='sitemap_html'),
    path('privacy_policy', privacy_policy, name='privacy_policy'),

]
