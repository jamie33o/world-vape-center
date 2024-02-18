from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from products.models import Product

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class ShippingAddress(models.Model):
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    eircode = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='user_address')

    class Meta:

        verbose_name_plural = 'Shipping Address'

    def __str__(self):

        return 'Shipping Address - ' + str(self.id)


class Favourite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)