from profile.models import Favourite
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.forms import AddToCartForm

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
        category_instance = get_object_or_404(Category,
                                              slug=category) if category \
            else Category.objects.first()
        category_products = Product.objects.\
            filter(category=category_instance)

        filters_form = FiltersForm(request.GET)
        if filters_form.is_valid():
            brands = filters_form.cleaned_data.get('brands')
            multi_options = filters_form.cleaned_data.get('multi_options')

            if brands:
                category_products = category_products.\
                    filter(brand__slug__in=[brand.slug for brand in brands])

            if multi_options:
                category_products = category_products.\
                    filter(options__slug__in=multi_options)

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
        form = AddToCartForm(
                product_id=product.id,
                product_options=product.options.all(),
                product_option_name=product.options_name
               )

        context = {
            'product': product,
            'reviews': reviews,
            'category_products': category_products,
            'form': form
        }

        return render(request, self.template_name, context)


class ReviewsView(View):
    """
    View for handling product reviews.

    Supports creating and updating reviews through POST requests,
    and deleting reviews through DELETE requests.

    Methods:
        post(request, product_id): Handles creating or
        updating reviews based on the provided form data.
        delete(request, review_id): Handles deleting
        reviews based on the provided review ID.
    """

    def post(self, request, product_id):
        """
        Handle the creation or update of product reviews.

        Parameters:
            request (HttpRequest): The incoming HTTP request.
            product_id (int): The ID of the product for
            which the review is created or updated.

        Returns:
            JsonResponse: A JSON response indicating
            the success or failure of the review creation or update.
        """
        try:
            form = ReviewForm(request.POST)
            product = get_object_or_404(Product, id=product_id)

            if form.is_valid():
                existing_review = Review.objects.\
                 filter(product=product, user=request.user).first()

                if existing_review:
                    existing_review.comment = form.cleaned_data['comment']
                    existing_review.rating = form.cleaned_data['rating']
                    existing_review.save()
                    return JsonResponse({'status': 'success',
                                         'message':
                                             'Review updated successfully'},
                                        status=200)
                else:
                    new_review = form.save(commit=False)
                    new_review.product = product
                    new_review.user = request.user
                    new_review.save()
                    return JsonResponse({'status': 'success',
                                         'message':
                                             'Thank you for your review'},
                                        status=200)

            return JsonResponse({'status': 'error',
                                 'message': form.errors},
                                status=400)

        except Exception as e:
            return JsonResponse({'status': 'error',
                                 'message': str(e)},
                                status=500)

    def delete(self, request, review_id):
        """
        Handle the deletion of product reviews.

        Parameters:
            request (HttpRequest): The incoming HTTP request.
            review_id (int): The ID of the review to be deleted.

        Returns:
            JsonResponse: A JSON response indicating the
            success or failure of the review deletion.
        """
        try:
            review = get_object_or_404(Review, id=review_id)

            if review.user == request.user:
                review.delete()
                return JsonResponse({'status': 'success',
                                     'message': 'Review deleted successfully'},
                                    status=200)
            else:
                return JsonResponse({'status': 'error',
                                     'message':
                                         'You do not have permission'
                                         'to delete this review'},
                                    status=403)

        except Exception as e:
            return JsonResponse({'status': 'error',
                                 'message': str(e)},
                                status=500)


def search(request):
    """
    Perform a product search based on the provided query parameter.

    Parameters:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing a
        list of product data matching the search query.
    """
    try:
        query = request.GET.get('q', '')
        results = []

        if query:
            products = Product.objects.filter(slug__icontains=query)[:5]

            for product in products:
                product_data = {
                    'url': reverse('product_details',
                                   args=[product.category.slug, product.slug]),
                    'name': product.name,
                    'price': product.price,
                    'img': product.image.url
                }
                results.append(product_data)

        return JsonResponse({'products': results})

    except Exception as e:
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=500)


@login_required
def add_to_favorites(request, product_id):
    """
    Add or remove a product from the user's favorites.

    Requires the user to be logged in.

    Parameters:
        request (HttpRequest): The incoming HTTP request.
        product_id (int): The ID of the product
        to be added or removed from favorites.

    Returns:
        JsonResponse: A JSON response indicating
        the status and message of the operation.
    """
    try:
        user = request.user
        product = get_object_or_404(Product, id=product_id)

        # Attempt to get an existing favorite for the user
        favourite, _ = Favourite.objects.get_or_create(user=user)

        # Check if the product is already favorited
        is_favourite = favourite.products.filter(id=product.id).exists()

        if not is_favourite:
            favourite.products.add(product)
            response_data = {'status': 'success',
                             'message': 'Product added to favourites.'}
            status_code = 200
        else:
            # If the product is already favorited, remove it
            favourite.products.remove(product)
            response_data = {'status': 'success',
                             'message': 'Product removed from favourites.'}
            status_code = 200

        return JsonResponse(response_data, status=status_code)

    except Exception:
        response_data = {'status': 'error',
                         'message': 'An error occurred while processing \
                            your request. Please try again later.'}
        status_code = 500

        return JsonResponse(response_data, status=status_code)
