from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.utils.text import slugify


class Category(models.Model):
    """
    Model representing a product category.

    Attributes:
    - name (str): The name of the category.
    - slug (str): The slugified version of the category name.

    Methods:
    - __str__(): Returns a string representation of the category.

    Meta:
    - verbose_name_plural (str): The plural name for the category model.
    """
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the category.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    """
    Model representing a product brand.

    Attributes:
    - name (str): The name of the brand.
    - slug (str): The slugified version of the brand name.

    Methods:
    - save(): Overrides the save method to automatically generate a slug.

    Meta:
    - verbose_name_plural (str): The plural name for the brand model.
    """
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the brand.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Brands'


class MultiOption(models.Model):
    """
    Model representing a multi-option for products.

    Attributes:
    - name (str): The name of the multi-option.
    - slug (str): The slugified version of the multi-option name.

    Methods:
    - save(): Overrides the save method to automatically generate a slug.

    """
    name = models.CharField(max_length=254, default='')
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the multi-option.
        """
        return self.name


class Product(models.Model):
    """
    Model representing a product.

    Attributes:
    - category (Category): The category to which the product belongs.
    - slug (str): The slugified version of the product name.
    - sku (str): The stock keeping unit of the product.
    - name (str): The name of the product.
    - image_url (str): The URL of the product image.
    - image (ImageField): The image file of the product.
    - brand (Brand): The brand of the product.
    - description (str): The description of the product.
    - price (Decimal): The original price of the product.
    - discounted_price (Decimal): The discounted price of the product.
    - countInStock (int): The quantity of the product in stock.
    - free_shipping (bool): Indicates if shipping is free for the product.
    - discount_percentage (str): The discount percentage of the product.
    - options_name (str): The name of the options for the product.
    - options (MultiOption): The multi-options associated with the product.

    Methods:
    - __str__(): Returns a string representation of the product.
    - num_reviews(): Returns the number of reviews for the product.
    - save(): Overrides the save method to automatically generate a slug.
    - average_rating(): Calculates the average rating of the product's reviews.

    """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.ForeignKey('Brand',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              )
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    free_shipping = models.BooleanField(default=False,
                                        help_text='Is shipping free?')
    discount_percentage = models.CharField(max_length=254,
                                           null=True, blank=True)
    options_name = models.CharField(max_length=254, null=True, blank=True)
    options = models.ManyToManyField(MultiOption, blank=True)

    def __str__(self):
        """
        Returns a string representation of the product.
        """
        return self.name

    def num_reviews(self):
        """
        Returns the number of reviews for the product.
        """
        return self.review_set.count()

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug.
        """
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def average_rating(self):
        """
        Calculates the average rating of the product's reviews.

        Returns:
        - int: The average rating, rounded.

        """
        average_rating = Review.objects.filter(product=self)\
            .aggregate(Avg('rating'))['rating__avg']
        return round(average_rating) if average_rating is not None else 0


class Review(models.Model):
    """
    Model representing a product review.

    Attributes:
    - product (Product): The product to which the review belongs.
    - user (User): The user who wrote the review.
    - name (str): The name associated with the review.
    - rating (int): The rating given in the review.
    - comment (str): The comment provided in the review.
    - created_at (DateTime): The date and time when the review was created.

    Methods:
    - __str__(): Returns a string representation of the rating.

    """
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the rating.
        """
        return str(self.rating)
