from django.urls import path
from .views import ProfileView, shipping_address_view, signin_view, signup_view

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('shipping_address_view/', shipping_address_view, name='shipping_address_view'),
    path('sign_in/', signin_view, name='sign_in'),
    path('sign_up/', signup_view, name='sign_up'),
]
