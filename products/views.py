from django.shortcuts import render
from django.views import View
from .models import Product


class OffersView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'products/products-list.html'

    def get(self, request):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        
        offers_products = Product.objects.filter(category__name='offers')

        context = {
            'products': offers_products,
        }
        return render(request, self.template_name, context)