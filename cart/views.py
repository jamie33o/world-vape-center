from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from cart.forms import AddToCartForm
from .cart import Cart


def cart_summary(request):
    """
    Display a summary of the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'cart-summary.html' template.

    Note:
        Ensure that the 'cart' context processor is added to the Django settings.
    """
    try:
        cart = Cart(request)

        discounted_products = Product.objects.filter(discounted_price__gt=0)

        return render(request, 'cart/cart-summary.html', {
            'cart': cart,
            'discounted_products': discounted_products,
        })
    except Exception:
        messages.error(request,
                       'Error trying to retrieve cart summary!!! Please contact us!!!')
        return redirect('contact_us')


@require_POST
def cart_add(request):
    """
    Add a product to the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the specified URL.

    """
    try:
        cart = Cart(request)
        form = AddToCartForm(request.POST)

        if form.is_valid():
            redirect_url = request.POST.get('redirect_url')
            product_quantity = form.cleaned_data['product_quantity']
            product_choice = request.POST.get('options')
            product_id = form.cleaned_data['product_id']

            product = get_object_or_404(Product, id=product_id)

            cart.add(product=product,
                     product_qty=int(product_quantity),
                     product_choice=product_choice)

            return redirect(redirect_url)

        messages.error(request,
                       f'Could not add product to cart: {form.errors}')
        return redirect('cart-summary')
    except Exception:
        messages.error(request, 'Could not add product to cart')
        return redirect('cart-summary')


@require_POST
def cart_delete(request):
    """
    Delete a product from the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'cart-summary' page.

    """
    try:
        cart = Cart(request)

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        messages.success(request, 'Product removed!!!')
        return redirect('cart-summary')
    except Exception:
        messages.error(request, 'Could not remove product')
        return redirect('cart-summary')


@require_POST
def cart_update(request):
    """
    Update the quantity of a product in the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'cart-summary' page.

    """
    try:
        cart = Cart(request)

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, qty=product_quantity)

        messages.success(request, 'Quantity updated!!!')
        return redirect('cart-summary')
    except Exception:

        messages.error(request, 'Could not update quantity')
        return redirect('cart-summary')