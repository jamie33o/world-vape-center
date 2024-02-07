from django.shortcuts import render
from django.views import View
from django.db.models import Avg
from products.models import Product
from .models import HomePage
from products.models import Category




class IndexView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'home/index.html'

    def get(self, request):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        
        homepage_instance = HomePage.objects.first()
        top_rated_products = Product.objects.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=3)
        if len(top_rated_products) < 10:
            categories = Category.objects.all()

            # Create a list to store the selected products
            top_rated_products = []

            # Iterate through each category
            for category in categories:
                # Query two products from the current category
                products_in_category = Product.objects.filter(category=category)[:2]

                # Add the products to the selected list
                top_rated_products.extend(products_in_category)


        context = {
            'homepage_instance': homepage_instance,
            'top_rated_products': top_rated_products,
        }
        return render(request, self.template_name, context)