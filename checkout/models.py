from profile.models import ShippingAddress
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


class Order(models.Model):
    """
    Model representing an order made by a user.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )
    full_name = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES, default='draft')
    shipping_address = models.ForeignKey(ShippingAddress,
                                         on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32,
                                    unique=True, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        null=False, default=0)
    sub_total = models.DecimalField(max_digits=10,
                                    decimal_places=2, null=False, default=0)
    discount = models.DecimalField(max_digits=10,
                                   decimal_places=2, null=True, default=0)
    grand_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=False, default=0)
    stripe_pid = models.CharField(max_length=254,
                                  null=False, blank=False, default='')
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             null=True, related_name='user_orders')


class OrderLineItem(models.Model):
    """
    Model representing a line item in an order.
    """
    order = models.ForeignKey(Order, null=False,
                              blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product,
                                null=False,
                                blank=False, on_delete=models.CASCADE)
    product_option = models.CharField(max_length=100,
                                      null=True, blank=True)
    quantity = models.IntegerField(null=False,
                                   blank=False, default=1)
    lineitem_total = models.DecimalField(max_digits=6,
                                         decimal_places=2,
                                         null=False,
                                         blank=False,
                                         editable=False)

    def __str__(self):
        return f'{self.quantity}x {self.product.name}\
              in Order #{self.order.order_number}'
