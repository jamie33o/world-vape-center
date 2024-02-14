from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Review, Category
from .forms import ReviewForm, FiltersForm


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
        category_instance = get_object_or_404(Category, slug=category) if category else Category.objects.first()
        category_products = Product.objects.filter(category=category_instance)
                
        filters_form = FiltersForm(request.GET)
        if filters_form.is_valid():
            brands = filters_form.cleaned_data.get('brands')
            multi_options = filters_form.cleaned_data.get('multi_options')

            if brands:
                category_products = category_products.filter(brand__slug__in=[brand.slug for brand in brands])

            if multi_options:
                category_products = category_products.filter(options__slug__in=multi_options)


        # Default number of items per page
        items_per_page = request.session.get('items_per_page', 24)

        # If the form is submitted with a new value, update the session
        if 'items_per_page' in request.GET:
            items_per_page = int(request.GET['items_per_page'])
            request.session['items_per_page'] = items_per_page


        paginator = Paginator(category_products, items_per_page)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            products = paginator.page(paginator.num_pages)


        context = {
            'products': products,
            'category': category_instance,
            'items_per_page': items_per_page,

        }
        return render(request, self.template_name, context)


class ProductDetailView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'products/product-details.html'

    def get(self, request, slug, *args, **kwargs):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        
        product = get_object_or_404(Product, slug=slug)
        reviews = Review.objects.filter(product=product)
        category_products = Product.objects.filter(category=product.category)

        context = {
            'product': product,
            'reviews': reviews,
            'category_products': category_products
        }

        return render(request, self.template_name, context)


class ReviewsView(View):

    def post(self, request, product_id):
        form = ReviewForm(request.POST)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            # Check if a review already exists for the user and product
            existing_review = Review.objects.filter(product=product, user=request.user).first()

            if existing_review:
                # If review exists, update the existing one
                existing_review.comment = form.cleaned_data['comment']
                existing_review.rating = form.cleaned_data['rating']
                existing_review.save()
                return JsonResponse({'status': 'success', 'message': 'Review updated successfully'}, status=200)
            else:
                # If review does not exist, create a new one
                new_review = form.save(commit=False)
                new_review.product = product
                new_review.user = request.user
                new_review.save()
                return JsonResponse({'status': 'success', 'message': 'Thank you for your review'}, status=200)
        return JsonResponse({'status': 'error', 'message': form.errors}, status=400)


    def delete(self, request, review_id):

        review = get_object_or_404(Review, id=review_id)

        # Check if the user deleting the review is the owner of the review
        if review.user == request.user:
            review.delete()
            return JsonResponse({'status': 'success', 'message': 'Review deleted successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this review'}, status=403)