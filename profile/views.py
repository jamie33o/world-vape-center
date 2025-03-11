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
from dashboard.forms import TicketForm, TicketResponseForm
from dashboard.models import Ticket

from .models import Favourite, ShippingAddress
from .forms import ShippingAddressForm, ProfileUpdateForm
from .forms import SignupForm, SigninForm


@login_required
def profile_view(request):

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile Updated!!')
        else:
            messages.error(request, user_form.errors)
        return redirect('profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)

    context = {
            'user_form': user_form,
        }
    
    return render(request, 'profile/profile.html', context)
 

@login_required
def shipping_address_view(request):
    """
    Handle displaying and updating the user's shipping address.

    - GET: Displays the shipping address form pre-filled with existing data.
    - POST: Updates the shipping address if the form is valid.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirects to 'profile' after successful update or renders the form on GET.
    """
    user_address_instance = request.user.user_address.first()

    if request.method == "POST":
        if user_address_instance is None:
            user_address_instance = ShippingAddress(user=request.user)

        shipping_address_form = ShippingAddressForm(request.POST, instance=user_address_instance)

        if shipping_address_form.is_valid():
            shipping_address_form.save()
            messages.success(request, "Shipping Address Updated!")
            return redirect("shipping_address_view")
        else:
            messages.error(request, "Error updating shipping address. Please check the form.")

    else:
        # GET request: Populate the form with existing address data
        shipping_address_form = ShippingAddressForm(instance=user_address_instance)

    return render(request, "profile/address.html", {"form": shipping_address_form})

@login_required
def favourites_view(request):
    """
    Handle displaying the user's favourite products.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered favourites page.
    """
    try:
        favourites = Favourite.objects.get(user=request.user)
        favourite_products = favourites.products.all()
    except Favourite.DoesNotExist:
        favourites = None
        favourite_products = None

    return render(request, 'profile/favourites.html', {'favourites': favourite_products})

@login_required
def orders_view(request):
    """
    Handle displaying the user's orders.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered orders page.
    """
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'profile/orders.html', {'user_orders': user_orders})


@login_required
def tickets_view(request):
    """
    Handle displaying the user's tickets.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered tickets page.
    """
    ticket_form = TicketForm()

    ticket_response_form = TicketResponseForm()

    user_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

    context ={
    'ticket_response_form': ticket_response_form,
    'ticket_form': ticket_form,
    'user_tickets': user_tickets
    }

    return render(request, 'profile/tickets.html', context)

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
