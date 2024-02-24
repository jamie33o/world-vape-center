from .cart import Cart

def cart(request):
    """
    Retrieve the cart object for the current request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the 'cart' key with the Cart object.

    Example:
        In a Django template, you can access the cart object using {{ cart }}.


    """
    return {'cart': Cart(request)}
