"""
Admin configuration for the 'profile' app.

This module defines the admin configuration
for the 'profile' app, including
custom admin classes for user-related models.

Contents:
- CustomUserAdmin: Admin class for the CustomUser model.
- ShippingAddressAdmin: Admin class for the ShippingAddress model.
- FavouriteAdmin: Admin class for the Favourite model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ShippingAddress, Favourite

class CustomUserAdmin(UserAdmin):
    """
    Admin class for the CustomUser model.

    Attributes:
    - model (Model): The CustomUser model.
    - list_display (list): The fields to display in the list view.
    """

    model = CustomUser
    list_display = ['first_name',
                    'last_name',
                    'username',
                    'email',
                    'profile_image']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Favourite)
