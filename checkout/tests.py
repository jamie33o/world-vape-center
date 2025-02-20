import json
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from .webhook_handler import StripeWH_Handler

class TestHandlePaymentIntentSucceeded(TestCase):
    @patch('stripe.Charge.retrieve')
    @patch('time.sleep')
    @patch('checkout.models.Order.objects.get')
    @patch('checkout.models.Order.objects.create')
    @patch('checkout.models.ShippingAddress.objects.create')
    @patch('products.models.Product.objects.get')
    def test_handle_payment_intent_succeeded_success(self, mock_product_get, mock_shipping_create, mock_order_create, mock_order_get, mock_sleep, mock_stripe_charge):
        # Mock data
        event_data = {
            'object': {
                'id': 'sample_id',
            'metadata': {
                'cart': '{"1": {"qty": 2, "price": 10}, "2": {"qty": 1, "price": 5}}',
                'order_num': '123456',
                'order_delivery': 5.00,
                'order_subtotal': 25.00,
                'order_discount': 0.00
            },
            'latest_charge': 'sample_charge_id',
            'shipping': {
                'phone': '1234567890',
                'address': {
                    'postal_code': '12345',
                    'city': 'Sample City',
                    'line1': '123 Sample St',
                    'line2': 'Apt 1',
                    'state': 'Sample State'
                }
            }
        }
        }
        event = MagicMock(data=MagicMock(object=event_data), type='payment_intent.succeeded')
        mock_stripe_charge.return_value = MagicMock(billing_details=MagicMock(email='test@example.com'), amount=2500)
        mock_order_get.side_effect = [MagicMock(), MagicMock()]
        mock_product_get.side_effect = [MagicMock(), MagicMock()]
        # Initialize the class instance
        request = MagicMock()  # Mocking the request object
        instance = StripeWH_Handler(request)

        # Call the function
        response = instance.handle_payment_intent_succeeded(event)

        # Assertions
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Webhook received: payment_intent.succeeded | SUCCESS: Created order in webhook', response.content.decode())
        mock_order_create.assert_called_once()
        mock_shipping_create.assert_called_once()
        self.assertEqual(mock_product_get.call_count, 2)
        self.assertEqual(mock_order_get.call_count, 2)

    @patch('stripe.Charge.retrieve')
    @patch('time.sleep')
    @patch('checkout.models.Order.objects.get')
    def test_handle_payment_intent_succeeded_existing_order(self, mock_order_get, mock_sleep, mock_stripe_charge):
        # Mock data
        event_data = {
            'object': {
                'id': 'sample_id',
            'metadata': {
                'cart': '{"1": {"qty": 2, "price": 10}, "2": {"qty": 1, "price": 5}}',
                'order_num': '123456',
                'order_delivery': 5.00,
                'order_subtotal': 25.00,
                'order_discount': 0.00
            },
            'latest_charge': 'sample_charge_id',
            'shipping': {
                'phone': '1234567890',
                'address': {
                    'postal_code': '12345',
                    'city': 'Sample City',
                    'line1': '123 Sample St',
                    'line2': 'Apt 1',
                    'state': 'Sample State'
                }
            }
        }
        }
        event = MagicMock(data=MagicMock(object=event_data), type='payment_intent.succeeded')
        mock_order_get.side_effect = [MagicMock(), MagicMock()]
        # Initialize the class instance
        request = MagicMock()  # Mocking the request object
        instance = StripeWH_Handler(request)

        # Call the function
        response = instance.handle_payment_intent_succeeded(event)

        # Assertions
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Webhook received: payment_intent.succeeded | SUCCESS: Verified order already in database', response.content.decode())
        self.assertEqual(mock_order_get.call_count, 1)
