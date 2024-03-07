from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.db.models import Avg
from products.models import Product
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

        try:
            # Query top-rated products with average rating greater than or equal to 3
            top_rated_products = Product.objects.annotate(
                avg_rating=Avg('review__rating')
            ).filter(avg_rating__gte=3)

            if len(top_rated_products) < 10:
                # Query all categories
                categories = Category.objects.all()

                # Create a list to store the selected products
                selected_products = []

                # Iterate through each category
                for category in categories:
                    # Query two products from the current category
                    products_in_category = Product.objects.\
                        filter(category=category)[:2]

                    # Add the products to the selected list
                    selected_products.extend(products_in_category)

                # Update the top_rated_products variable
                top_rated_products = selected_products

        except Exception:
            messages.error(request, 'Error retrieving top rated products')

        # Prepare context for rendering the template
        context = {
            'top_rated_products': top_rated_products,
        }

        # Render the template with the context
        return render(request, self.template_name, context)
