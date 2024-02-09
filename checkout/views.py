from decimal import Decimal
import json
import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from products.models import Product
from cart.cart import Cart
from .forms import ShippingDetailsForm
from .models import Order, OrderLineItem
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings




@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'order_num': json.dumps(request.session.get('order_num', {})),

        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = Cart(request)

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'eircode': request.POST['eircode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        shipping_form = ShippingDetailsForm(form_data)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.save()
            
            order = Order()

            pid = request.POST.get('client_secret').split('_secret')[0]

            order.stripe_pid = pid
            order.shipping_address = address
            order.delivery_cost = cart.get_delivery_cost()
            order.order_total = cart.get_total()
            order.grand_total = cart.get_grand_total()
            order.order_number = cart.get_order_num()
            order.save()
            
            user = request.user if request.user.is_authenticated else None

            for item_id, item_data in cart.cart.items():
                if item_data.get('discounted_price'):
                    total = Decimal(item_data['discounted_price']) * item_data['qty']
                else:
                    total = Decimal(item_data['price']) * item_data['qty']

                try:
                    product = Product.objects.get(id=item_id)
                    
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data['qty'],
                        lineitem_total=total,
                        user= user
                    )
                    if item_data.get('product_choice'):
                        order_line_item.product_option=item_data['product_choice'],

                    order_line_item.save()
                    
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()

                    return redirect(reverse('cart-summary'))
                
            email_customer(request.POST['email'], 'Order Received')

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = Cart(request)
        if not cart:
            messages.info(request, "There's nothing in your cart at the moment")
            return redirect(reverse('cart-summary'))


        total = cart.__len__()
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = ShippingDetailsForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.shipping_address.email} .')

    if 'cart' in request.session:
        del request.session['cart']
        del request.session['order_num']

    template = 'checkout/checkout-success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def email_customer( email, email_subject):

        email_content = render_to_string('checkout/order_received_email.html')
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            email_subject,
            '',
            from_email,
            [email],
            html_message=email_content,
            fail_silently=False
        )