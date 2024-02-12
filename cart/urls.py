from django.urls import path
from .views import cart_add, cart_delete, cart_summary, cart_update

urlpatterns = [
    path('', cart_summary, name='cart-summary'),
    path('add/', cart_add, name='cart-add'),
    path('delete/', cart_delete, name='cart-delete'),
    path('update/', cart_update, name='cart-update'),
]
