# products/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Product, Category

class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Product.objects.all()
    
    def location(self, item):
        # Modify this based on your URL structure
        return f'/products/{item.category.slug}/{item.slug}/'
    

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Category.objects.all()
    
    def location(self, item):
        # Modify this based on your URL structure
        return f'/products/{item.slug}/'