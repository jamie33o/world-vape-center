# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ShippingAddress, Favourite

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['first_name', 'last_name', 'username', 'email', 'profile_image']  # Adjust as needed

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Favourite)