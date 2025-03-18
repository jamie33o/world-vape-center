from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product, ProductVariant
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
        Ensure that the 'cart' context processor
        is added to the Django settings.
    """
    try:
        cart = Cart(request)

        discounted_products = Product.objects.filter(discounted_price__gt=0)

        return render(request, 'cart/cart-summary.html', {
            'cart': cart,
            'discounted_products': discounted_products,
        })
    except Exception as e:
        print(e)
        messages.error(request,
                       'Error trying to retrieve cart \
                       summary!!! Please contact us!!!')
        return redirect('contact_us')


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the specified URL.

    """
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = AddToCartForm(request.POST, product=product)

        if form.is_valid():
            selected_variants = {
                variant_type: form.cleaned_data[variant_type]
                for variant_type in product.get_variant_options().keys()
            }
            
            quantity = form.cleaned_data["quantity"]
            
            # Find the matching variant
            variant = ProductVariant.objects.filter(
                product=product,
                name__in=selected_variants.values()
            ).first()
            
            cart.add(product_qty=int(quantity),
                     product_variant=variant)
            messages.success(request,
                            'Product added to cart')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.error(request,
                       f'Could not add product to cart: {form.errors}')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        print(e)
        messages.error(request, 'Could not add product to cart')
        return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def cart_delete(request, sku):
    """
    Delete a product from the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'cart-summary' page.

    """
    try:
        cart = Cart(request)

        cart.delete(sku=sku)
        messages.success(request, 'Product removed!!!')
        return redirect('cart-summary')
    except Exception:
        messages.error(request, f'{e}Could not remove product')
        return redirect('cart-summary')


@require_POST
def cart_update(request, sku):
    """
    Update the quantity of a product in the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'cart-summary' page.

    """
    try:
        cart = Cart(request)

        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(sku=sku, qty=product_quantity)

        messages.success(request, 'Quantity updated!!!')
        return redirect('cart-summary')
    except Exception:

        messages.error(request, 'Could not update quantity')
        return redirect('cart-summary')
