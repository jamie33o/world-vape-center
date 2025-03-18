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

    def has_variants(self):
        """
        Returns True if the product has variants.
        """
        return self.variants.exists()
    
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
        if not self.sku:
            self.sku = f"{self.name}-{self.id}"  # Assigns SKU for the main product
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
        Returns a dictionary where keys are human-readable variant types (e.g., 'Color', 'Size')
        and values are lists of available options for each type.
        """
        variants = self.variants.all()  # Get all variants for this product
        variant_dict = {}

        # Convert VARIANT_CHOICES into a dictionary for easy lookup
        variant_type_dict = dict(ProductVariant.VARIANT_CHOICES)  # {'color': 'Color', 'size': 'Size'}

        for variant in variants:
            # Get human-readable name for the variant type
            variant_label = variant_type_dict.get(variant.variant_type, variant.variant_type)  # Default to key if not found

            if variant_label not in variant_dict:
                variant_dict[variant_label] = []

            if variant.name not in variant_dict[variant_label]:
                variant_dict[variant_label].append(variant.name)

        return variant_dict  # Example: {'Color': ['Red', 'Blue'], 'Size': ['Small', 'Large']}



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
    VARIANT_CHOICES = [
        ('flavor', 'Flavor'),
        ('nicotine', 'Nicotine Strength'),
        ('size', 'Size'),
        ('color', 'Color'),
    ]
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    variant_type = models.CharField(max_length=50, choices=VARIANT_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    sku = models.CharField(max_length=254, unique=True, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    additional_info = models.TextField(null=True, blank=True)

    def variant_count(self):
        """
        Returns the count of products having this variant.
        """
        return ProductVariant.objects.filter(variant_type=self.variant_type, name=self.name).count()

    def save(self, *args, **kwargs):
        """
        Automatically generate SKU if not provided.
        """
        if not self.sku:
            self.sku = f"{self.product.slug}-{self.variant_type}-{self.name}".replace(" ", "-").upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.variant_type}: {self.name}"


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
