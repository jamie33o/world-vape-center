import json
import time
from decimal import Decimal
import stripe

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from products.models import Product
from .models import Order, OrderLineItem, ShippingAddress


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        order_num = intent.metadata.order_num
        try:
            stripe_charge = stripe.Charge.retrieve(
                intent.latest_charge
            )

            billing_details = stripe_charge.billing_details
            shipping_details = intent.shipping
            grand_total = round(stripe_charge.amount / 100, 2)
            
        except Exception as e:
            print(e)
        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(order_number=order_num)
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            context = {
                'order': order
            }
            self.email_customer(billing_details.email, context,
                'Order Successfull')
            return HttpResponse(
                content=f'Webhook received: {event["type"]}'
                '| SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                address = ShippingAddress(
                    phone_number=shipping_details.phone,
                    eircode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                )
                address.save()

                order = Order()

                order.stripe_pid = pid
                order.shipping_address = address
                order.full_name = billing_details.name
                order.email = billing_details.email
                # order.delivery_cost = cart.get_delivery_cost()
                # order.sub_total = cart.get_subtotal()
                order.grand_total = grand_total
                order.order_number = order_num
                order.save()

                for item_id, item_data in json.loads(cart).items():
                    if item_data.get('discounted_price'):
                        total = Decimal(item_data['discounted_price'])\
                        * item_data['qty']
                    else:
                        total = Decimal(item_data['price']) * item_data['qty']

                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data['qty'],
                        lineitem_total=total,
                        product_option=item_data['product_choice'] if item_data.get('product_choice') else None,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        context = {
                'order': order
            }
        self.email_customer(billing_details.email, context,
                'Order Successfull')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}'
            '| SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def email_customer(self, email, context, email_subject):
        """
        Send an email to the customer.

        Args:
            email (str): The customer's email address.
            email_subject (str): The subject of the email.

        Note:
            This function sends an email to the customer
            using the provided email address and subject.
            The email content is rendered from the
            'checkout/order_received_email.html' template.
    """
        email_content = render_to_string('checkout/order_success_email.html',
                                         context)
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            email_subject,
            '',
            from_email,
            [email],
            html_message=email_content,
            fail_silently=False
        )
