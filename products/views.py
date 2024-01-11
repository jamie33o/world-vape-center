from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Product, Review, Category
from .forms import ReviewForm



def all_categories(request):
    """
    Handle GET requests to display the list of categories.

    Returns:
        HttpResponse: Rendered template with channel information.
    """
    categories = Category.objects.all()


    context = {
        'all_categories': categories
    }
    return context
    

class CategoryView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'products/products-list.html'

    def get(self, request, category=None):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        category_instance = get_object_or_404(Category, name=category) if category else Category.objects.first()
        category_products = Product.objects.filter(category=category_instance)

        context = {
            'products': category_products,
        }
        return render(request, self.template_name, context)
    

class ProductDetailView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'products/product-details.html'

    def get(self, request, product_id):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        
        product = get_object_or_404(Product, id=product_id)
        reviews = Review.objects.filter(product=product)

        context = {
            'product': product,
            'reviews': reviews
        }
        return render(request, self.template_name, context)
    


class ReviewsView(View):
    def post(self, request, product_id):
        form = ReviewForm(request.POST)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = product
            new_review.user = request.user 
            new_review.save()
            return JsonResponse({'status': 'success', 'message': 'Thank you for your feedback'}, status=200)
        return JsonResponse({'status': 'error', 'message': form.errors})
