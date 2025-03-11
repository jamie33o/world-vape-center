from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from products.models import Product


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Fields:
    - profile_image (ImageField): User's profile image.
    - date_of_birth (DateField): User's date of birth.
    """

    profile_image = models.ImageField(upload_to='profile_images/',
                                      null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class ShippingAddress(models.Model):
    """
    Model for storing user shipping addresses.

    Fields:
    - phone_number (CharField): Phone number for shipping.
    - street_address1 (CharField): First line of street address.
    - street_address2 (CharField, optional): Second line of street address.
    - town_or_city (CharField): Town or city for shipping.
    - county (CharField, optional): County for shipping.
    - eircode (CharField, optional): Eircode for shipping.
    - user (ForeignKey): Foreign key to the user associated with the address.
    """

    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    eircode = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             null=True, blank=True,
                             related_name='user_address')

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f"{self.user}'s  Shipping Address" if self.user else 'Shipping Address'


class Favourite(models.Model):
    """
    Model for storing user favorites.

    Fields:
    - user (ForeignKey): Foreign key to the user associated with the favorites.
    - products (ManyToManyField): Many-to-many relationship with Product model.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

