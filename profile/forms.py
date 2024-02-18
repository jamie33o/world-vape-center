from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import ShippingAddress, CustomUser


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_image']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['phone_number', 'street_address1', 'street_address2', 'town_or_city' , 'county', 'eircode']


class CheckoutDetailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth']

class SigninForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']