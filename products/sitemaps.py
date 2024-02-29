# products/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Product, Category


class ProductSitemap(Sitemap):
    """
    Sitemap for individual product details.

    Attributes:
    - changefreq (str): The anticipated frequency
    of changes to the content ('monthly').
    - priority (float): The priority of the content
    in relation to other content (0.9).

    Methods:
    - items(): Returns the queryset of products
    to be included in the sitemap.
    - location(item): Returns the URL location
    for a given product in the sitemap.

    Note:
    Modify the location method based on your actual URL structure.
    """

    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        """
        Returns the queryset of products to be included in the sitemap.
        """
        return Product.objects.all()

    def location(self, item):
        """
        Returns the URL location for a given product in the sitemap.

        Args:
        - item (Product): The product for which to generate the URL.

        Returns:
        - str: The URL location for the product in the sitemap.

        Note:
        Modify this based on your URL structure.
        """
        return f'/products/{item.category.slug}/{item.slug}/'


class CategorySitemap(Sitemap):
    """
    Sitemap for category pages.

    Attributes:
    - changefreq (str): The anticipated
    frequency of changes to the content ('monthly').
    - priority (float): The priority of the content
    in relation to other content (0.9).

    Methods:
    - items(): Returns the queryset of categories
    to be included in the sitemap.
    - location(item): Returns the URL location
    for a given category in the sitemap.

    Note:
    Modify the location method based on your actual URL structure.
    """

    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        """
        Returns the queryset of categories to be included in the sitemap.
        """
        return Category.objects.all()

    def location(self, item):
        """
        Returns the URL location for a given category in the sitemap.

        Args:
        - item (Category): The category for which to generate the URL.

        Returns:
        - str: The URL location for the category in the sitemap.

        Note:
        Modify this based on your URL structure.
        """
        return f'/products/{item.slug}/'
