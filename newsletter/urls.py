"""
url path for the newsletter app
"""
from django.urls import path
from .views import subscribe_newsletter

urlpatterns = [
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
]
