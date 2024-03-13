"""
Forms for handling user authentication and profile-related data.

This module defines various forms used in the application for handling user
authentication, profile updates, shipping addresses, checkout details, and
user sign-up.

Contents:
- ProfileUpdateForm: Form for updating user profile information.
- ShippingAddressForm: Form for handling user shipping address.
- CheckoutDetailForm: Form for handling checkout details.
- SignupForm: Form for user sign-up.
- SigninForm: Form for user sign-in.

"""
from django import forms
from django.forms import DateInput

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ShippingAddress, CustomUser


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Fields:
    - first_name (CharField): User's first name.
    - last_name (CharField): User's last name.
    - username (CharField): User's username.
    - email (EmailField): User's email address.
    - profile_image (ImageField): User's profile image.
    - date_of_birth (DateField): User's date of birth.
    """

    class Meta:
        """
        Meta class for ProfileUpdateForm.

        Specifies the model and fields to be included in the form.
        """
        model = CustomUser
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'profile_image',
                  'date_of_birth']

        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }



class ShippingAddressForm(forms.ModelForm):
    """
    Form for handling user shipping address.

    Fields:
    - phone_number (CharField): Phone number for shipping.
    - street_address1 (CharField): First line of street address.
    - street_address2 (CharField, optional): Second line of street address.
    - town_or_city (CharField): Town or city for shipping.
    - county (ChoiceField): County for shipping.
    - eircode (CharField, optional): Eircode for shipping.
    """

    COUNTY_CHOICES = [
        ('Antrim', 'Antrim'),
        ('Armagh', 'Armagh'),
        ('Carlow', 'Carlow'),
        ('Cavan', 'Cavan'),
        ('Clare', 'Clare'),
        ('Cork', 'Cork'),
        ('Derry', 'Derry'),
        ('Donegal', 'Donegal'),
        ('Down', 'Down'),
        ('Dublin', 'Dublin'),
        ('Fermanagh', 'Fermanagh'),
        ('Galway', 'Galway'),
        ('Kerry', 'Kerry'),
        ('Kildare', 'Kildare'),
        ('Kilkenny', 'Kilkenny'),
        ('Laois', 'Laois'),
        ('Leitrim', 'Leitrim'),
        ('Limerick', 'Limerick'),
        ('Longford', 'Longford'),
        ('Louth', 'Louth'),
        ('Mayo', 'Mayo'),
        ('Meath', 'Meath'),
        ('Monaghan', 'Monaghan'),
        ('Offaly', 'Offaly'),
        ('Roscommon', 'Roscommon'),
        ('Sligo', 'Sligo'),
        ('Tipperary', 'Tipperary'),
        ('Tyrone', 'Tyrone'),
        ('Waterford', 'Waterford'),
        ('Westmeath', 'Westmeath'),
        ('Wexford', 'Wexford'),
        ('Wicklow', 'Wicklow')
    ]

    phone_number = forms.CharField()
    street_address1 = forms.CharField()
    street_address2 = forms.CharField(required=False)
    town_or_city = forms.CharField()
    county = forms.ChoiceField(choices=COUNTY_CHOICES)
    eircode = forms.CharField(required=False)

    class Meta:
        """
        Meta class for ShippingAddressForm.

        Specifies the model and fields to be included in the form.
        """
        model = ShippingAddress
        fields = ['phone_number', 'street_address1', 'street_address2',
                  'town_or_city', 'county', 'eircode']



class CheckoutDetailForm(forms.ModelForm):
    """
    Form for handling checkout details.

    Fields:
    - first_name (CharField): User's first name.
    - last_name (CharField): User's last name.
    - email (EmailField): User's email address.
    """

    class Meta:
        """
        Meta class for CheckoutDetailForm.

        Specifies the model and fields to be included in the form.
        """
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(CheckoutDetailForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True


class SignupForm(UserCreationForm):
    """
    Form for user sign-up.

    Inherits from UserCreationForm and includes additional fields.

    Fields:
    - username (CharField): User's desired username.
    - email (EmailField): User's email address.
    - password1 (CharField): User's chosen password.
    - password2 (CharField): User's password confirmation.
    - date_of_birth (DateField): User's date of birth.
    """

    class Meta:
        """
        Meta class for SignupForm.

        Specifies the model and fields to be included in the form.
        """
        model = CustomUser
        fields = ['username', 'email',
                  'password1', 'password2', 'date_of_birth']


class SigninForm(AuthenticationForm):
    """
    Form for user sign-in.

    Inherits from AuthenticationForm.

    Fields:
    - username (CharField): User's username.
    - password (CharField): User's password.
    """

    class Meta:
        """
        Meta class for SigninForm.

        Specifies the model and fields to be included in the form.
        """
        model = CustomUser
        fields = ['username', 'password']
