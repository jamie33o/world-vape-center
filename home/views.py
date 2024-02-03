from django.shortcuts import render
from django.views import View
from django.db.models import Avg
from products.models import Product
from .models import HomePage



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


        context = {
            'homepage_instance': homepage_instance,
            'top_rated_products': top_rated_products,
        }
        return render(request, self.template_name, context)