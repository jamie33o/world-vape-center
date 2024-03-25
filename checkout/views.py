from decimal import Decimal
import json
from profile.forms import CheckoutDetailForm, ShippingAddressForm
from profile.forms import SigninForm, SignupForm
import stripe
from stripe.error import StripeError
from django.shortcuts import (render,
                              redirect,
                              reverse,
                              get_object_or_404,
                              HttpResponse)
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from products.models import Product
from dashboard.models import Ticket
from cart.cart import Cart
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    """
    Cache checkout data in the PaymentIntent metadata.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: HTTP response with status 200 if successful,
        400 if an error occurs.

    Note:
        This view is intended to be used with a Stripe
        PaymentIntent to cache additional data related to
        the checkout process.
        It extracts the PaymentIntent ID (pid) from the request's
        POST data and modifies the PaymentIntent metadata
        with cart information, username, and order number.
        If an error occurs, an error message is displayed,
        and an HTTP response with status 400 is returned.
    """
    try:
        cart = Cart(request)
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            stripe.PaymentIntent.modify(pid, metadata={
                'cart': json.dumps(cart.get_meta_data()),
                'username': str(request.user),  
                'order_num': json.dumps(request.session.get('order_num', {})),
                'order_delivery': cart.get_delivery_cost(),
                'order_subtotal': cart.get_subtotal(),
                'order_discount': cart.get_discounted_total(),
            })
            return HttpResponse(status=200)
        except StripeError as e:
            try:
                ticket = Ticket(title='site_error',
                                description=f'cache_checkout_data error: {e}',
                                user=request.user if request.user else None
                                )
                ticket.save()
                messages.error(request, 'We are very sorry, \
                        an unknown error occurred: But the Admin has been notified')

            except Exception:
                messages.error(request, 'We are very sorry, \
                        an unknown error occurred: Please contact us')
            return HttpResponse(status=400)

    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Process the checkout, handle form submissions,
    and render the checkout page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response for the checkout page.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    save_address =  request.POST.get('save-info')

    if request.method == 'POST':
        cart = Cart(request)

        shipping_form = ShippingAddressForm(request.POST)
        profile_detail_form = CheckoutDetailForm(request.POST)


        if shipping_form.is_valid() and profile_detail_form.is_valid():
            first_name = profile_detail_form.cleaned_data['first_name']
            last_name = profile_detail_form.cleaned_data['last_name']
            email = profile_detail_form.cleaned_data['email']
            address = shipping_form.save(commit=False)

            if save_address:
                user = request.user
                address.user = user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

            address.save()
            order = Order()
            user = request.user if request.user.is_authenticated else None
            if user:
                order.user = user

            pid = request.POST.get('client_secret').split('_secret')[0]

            order.status = 'pending'
            order.stripe_pid = pid
            order.full_name = f'{first_name} {last_name}'
            order.email = email
            order.shipping_address = address
            order.discount = cart.get_discounted_total()
            order.delivery_cost = cart.get_delivery_cost()
            order.sub_total = cart.get_subtotal()
            order.grand_total = cart.get_grand_total()
            order.order_number = cart.get_order_num()
            order.save()

            for item_id, item_data in cart.cart.items():
                if item_data.get('discounted_price'):
                    total = Decimal(item_data['discounted_price']) * \
                    item_data['qty']
                else:
                    total = Decimal(item_data['price']) * item_data['qty']
                try:
                    product = Product.objects.get(id=item_id)

                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data['qty'],
                        lineitem_total=total,
                    )

                    if item_data.get('product_choice'):
                        order_line_item.product_option = item_data['product_choice']

                    order_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database."
                        f"Please contact us for assistance! Your \
                            order number was {order.order_number} please send it aswell")
                    )

                    return redirect('contact_us')
            try:
                email_content = render_to_string('checkout/order_received_email.html')
                from_email = settings.EMAIL_HOST_USER
                send_mail(
                    'Order Received',
                    '',
                    from_email,
                    [email, ],
                    html_message=email_content,
                    fail_silently=False
                )
            except Exception as e:
                try:
                    ticket = Ticket(title='site_error',
                                    description=f'checkout function error: {e}',
                                    user=request.user if request.user else None
                                    )
                    ticket.save()
                    messages.error(request, 'We are very sorry, \
                            Could not send order success email:\
                                    But the Admin has been notified')

                except Exception:
                    messages.error(request, 'We are very sorry, \
                            an unknown error occurred: Please contact us')
            return redirect(reverse('checkout_success', args=[order.id]))
        else:
            if not shipping_form.is_valid():
                messages.error(request, shipping_form.errors)
            else:
                messages.error(request, profile_detail_form.errors)
            return redirect('checkout')
    else:
        cart = Cart(request)
        if not cart:
            messages.info(request,
                          "There's nothing in your cart at the moment")
            return redirect(reverse('cart-summary'))

        total = cart.get_grand_total()
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            user_address_instance = request.user.user_address.first()
            order_form = ShippingAddressForm(instance=user_address_instance)
            profile_detail_form = CheckoutDetailForm(instance=request.user)
        else:
            order_form = ShippingAddressForm()
            profile_detail_form = CheckoutDetailForm(auto_id='detail_%s')
            sign_up_form = SignupForm(auto_id='signup_%s')
            sign_in_form = SigninForm(auto_id='signin_%s')

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.\
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
        'profile_detail_form': profile_detail_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    if not request.user.is_authenticated:
        context['sign_up_form'] = sign_up_form
        context['sign_in_form'] = sign_in_form

    return render(request, template, context)


def checkout_success(request, order_id):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, id=order_id)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order.order_number}. A confirmation \
        email will be sent to {order.email} .')

    if 'cart' in request.session:
        del request.session['cart']
        del request.session['order_num']


    template = 'checkout/checkout-success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
