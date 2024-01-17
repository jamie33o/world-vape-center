from django.urls import path
from .views import subscribe_newsletter, un_subscribe_newsletter

urlpatterns = [
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('un_subscribe/', un_subscribe_newsletter, name='un_subscribe_newsletter'),

]
