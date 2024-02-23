from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.models import Product
from .cart import Cart



def cart_summary(request):

    cart = Cart(request)

    discounted_products = Product.objects.filter(discounted_price__gt=0)

    return render(request, 'cart/cart-summary.html',
                  {'cart':cart,
                   'discounted_products': discounted_products})



def cart_add(request):

    cart = Cart(request)

    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        product_id = int(request.POST.get('product_id'))

        product_quantity =  int(request.POST.get('product_quantity'))
        product_choice = request.POST.get('product_choice') if request.POST.get('product_choice') else None

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_qty=product_quantity, product_choice=product_choice)

        return redirect(redirect_url)
        


def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        messages.success(request, 'Product removed!!!')
        return redirect('cart-summary')
    messages.error(request, 'Could not remove product')
    return redirect('cart-summary')




def cart_update(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, qty=product_quantity)

        messages.success(request, 'Quantity updated!!!')
        return redirect('cart-summary')
    messages.error(request, 'Could not update quantity')
    return redirect('cart-summary')
