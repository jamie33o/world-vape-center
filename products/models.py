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
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(upload_to="categories", blank=True)


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

    def product_count(self):
        """
        Returns the count of products associated with this brand.
        """
        return Product.objects.filter(brand=self).count()

    def __str__(self):
        """
        Returns a string representation of the brand.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Brands'


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
    name = models.CharField(max_length=254)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    brand = models.ForeignKey('Brand',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              )
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)

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


    def get_variant_options(self):
        """
        Returns a dictionary where keys are variant types (e.g., color, size)
        and values are lists of available options for each type.
        """
        variants = self.variants.all()  # Get all variants for this product
        variant_dict = {}

        for variant in variants:
            if variant.variant_type not in variant_dict:
                variant_dict[variant.variant_type] = []
            if variant.name not in variant_dict[variant.variant_type]:
                variant_dict[variant.variant_type].append(variant.name)

        return variant_dict  # Example: {'color': ['Red', 'Blue'], 'size': ['Small', 'Large']}

class ProductVariant(models.Model):
    """
    Model representing a variant of a product.

    Attributes:
    - product (Product): The main product this variant belongs to.
    - sku (str): The stock keeping unit of the variant.
    - name (str): The name of the variant.
    - price (Decimal): The price of the variant.
    - discounted_price (Decimal): The discounted price of the variant.
    - countInStock (int): The quantity of the variant in stock.
    - additional_info (str): Additional information specific to the variant.

    Methods:
    - __str__(): Returns a string representation of the product variant.
    """
    OPTION_CHOICES = [
        ('flavor', 'Flavor'),
        ('nicotine', 'Nicotine Strength'),
        ('size', 'Size'),
        ('color', 'Color'),
    ]
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    variant_type = models.CharField(max_length=50, choices=OPTION_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    sku = models.CharField(max_length=254, unique=True, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    additional_info = models.TextField(null=True, blank=True)

    def variant_count(self):
        """
        Returns the count of products having this variant.
        """
        return ProductVariant.objects.filter(variant_type=self.variant_type, name=self.name).count()

    def __str__(self):
        return f"{self.name} - {self.variant_type} - Stock: {self.countInStock}"


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
