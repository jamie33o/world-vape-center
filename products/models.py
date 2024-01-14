from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg



class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'Brands'


class MultiOption(models.Model):
    options = models.JSONField(blank=True, null=True)


    def __str__(self):
        name = str(self.options)
        return name


class Product(models.Model):

    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.ForeignKey('Brand', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    free_shipping = models.BooleanField(default=False, help_text='Is shipping free?')
    discount_percentage = models.CharField(max_length=254, null=True, blank=True)
    option = models.ForeignKey('MultiOption', null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

    def num_reviews(self):
        return self.review_set.count()

    def average_rating(self):
        # Calculate the average rating for the product's reviews
        average_rating = Review.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']

        # If there are no reviews, return 0 or another default value
        return round(average_rating) if average_rating is not None else 0


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)