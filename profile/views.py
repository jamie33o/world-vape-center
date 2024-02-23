"""
Views for the Django application.

This module contains view functions and classes responsible for handling
HTTP requests and returning appropriate HTTP responses. Views define the
presentation layer of the application, determining how data is presented to
the user and handling user interactions.

Views in this module are organized based on their functionality, and each
view function or class corresponds to a specific URL endpoint or page in the
application.

Contents:
- ProfileView
- shipping_address_view
- signup_view
- signin_view
"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib import messages
from checkout.models import Order
from .models import Favourite, ShippingAddress
from .forms import ShippingAddressForm, ProfileUpdateForm
from .forms import SignupForm, SigninForm


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """
    Display and handle updates for the user's profile.

    This view allows users to view and update their profile information,
    including shipping address, orders, and favorites.

    Attributes:
    - template_name (str): The template used to render the profile page.
    """

    template_name = 'profile/base.html'

    def get(self, request):
        """
        Handle GET requests for the user's profile.

        Returns:
        - HttpResponse: Rendered profile page.
        """
        user_address_instance = request.user.user_address.first()

        user_form = ProfileUpdateForm(instance=request.user)
        shipping_address_form = ShippingAddressForm(instance=user_address_instance)
        user_orders = Order.objects.filter(user=request.user)

        try:
            favourites = Favourite.objects.get(user=request.user)
        except Favourite.DoesNotExist:
            favourites = None

        if favourites:
            favourite_products = favourites.products.all()
        else:
            favourite_products = None

        context = {
            'user_form': user_form,
            'shipping_address_form': shipping_address_form,
            'user_orders': user_orders,
            'favourites': favourite_products
        }

        return render(request, self.template_name, context)

    @method_decorator(require_POST)
    def post(self, request):
        """
        Handle POST requests for updating the user's profile.

        Returns:
        - HttpResponse: Redirects to the 'profile' page after updating the profile.
        """
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile Updated!!')
        else:
            messages.error(request, user_form.errors)

        return redirect('profile')


@require_POST
def shipping_address_view(request):
    """
    Handle updating the user's shipping address.

    This view processes a POST request for updating the user's shipping address.
    If the user doesn't have a shipping address, a new instance is created.
    The shipping address form is then populated with the user's address data,
    validated, and saved.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirects to the 'profile' page after updating the shipping address.
    """
    user_address_instance = request.user.user_address.first()

    if user_address_instance is None:
        # If the user doesn't have a shipping address, create a new instance
        user_address_instance = ShippingAddress(user=request.user)

    shipping_address_form = ShippingAddressForm(request.POST, instance=user_address_instance)

    if shipping_address_form.is_valid():
        shipping_address_form.save()
        messages.success(request, 'Shipping Address Updated!!')
    else:
        messages.error(request, 'Error updating shipping address. Please check the form.')

    return redirect('profile')



@require_POST
def signup_view(request):
    """
    Handle user sign-up.

    This view processes a POST request for user sign-up. It validates the
    signup form, creates a new user if the form is valid, logs in the user,
    and redirects to the specified URL after sign-up.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirects to the specified URL after sign-up.

    Raises:
    - Exception: Redirects to the 'contact_us' page with an error message if an
                unknown error occurs.
    """
    try:
        redirect_url = request.POST.get('redirect_url')
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signed up successfully')
            return redirect(redirect_url)

        messages.error(request, form.errors)
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'We are very sorry, \
                        an unknown error occurred: {e}... PLEASE CONTACT US!!!')
        return redirect('contact_us')


@require_POST
def signin_view(request):
    """
    Handle user sign-in.

    This view processes a POST request for user sign-in on the check out page.
    It validates the sign-in form, and logs in the user if the form is valid.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirects to the specified URL after sign-in.

    Raises:
    - Exception: Redirects to the 'contact_us' page with an error message if an
                unknown error occurs.
    """
    try:
        redirect_url = request.POST.get('redirect_url')
        form = SigninForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, 'Signed in successfully')
            return redirect(redirect_url)

        messages.error(request, form.errors)
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'We are very sorry. An \
                       unknown error occurred: {e}... PLEASE CONTACT US!!!')
        return redirect('contact_us')
