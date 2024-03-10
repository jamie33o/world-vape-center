import uuid
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product


class Cart():

    """
    Shopping Cart class to manage user's shopping cart.

    Attributes:
        session (dict): The session object from the request.
        cart (dict): The user's cart containing product details.
        order_num (str): The unique order number for the cart.
        cart_updated (dict): Dictionary to track if the cart is updated.
    """
    def __init__(self, request):
        """
        Initialize the Cart instance.

        Args:
            request (HttpRequest): The HTTP request object.

        """
        self.session = request.session

        cart = self.session.get('cart')
        order_num = self.session.get('order_num')
        cart_updated = self.session.get('cart_updated')

        # New user - generate a new session
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
            self.session['order_num'] = str(self._generate_order_number())
            self.session['cart_updated'] = {'cart_bool': False}
            order_num = self.session['order_num']
            cart_updated = self.session['cart_updated']

        self.cart = cart
        self.order_num = order_num
        self.cart_updated = cart_updated

    def add(self, product, product_qty, product_choice):
        """
        Add a product to the shopping cart.

        Args:
            product (Product): The product to be added.
            product_qty (int): The quantity of the product to be added.
            product_choice (str): The choice or
            option selected for the product.


        Note:
            If the product is already in the cart,
            the quantity will be updated.
            If the product is not in the cart, a new entry will be added.
            The session will be marked as modified to save the changes.
        """
        self.cart_updated['cart_bool'] = True

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty \
                if product_qty > 1 else self.cart[product_id]['qty'] + 1
        else:
            self.cart[product_id] = {'price': str(product.price),
                                     'qty': product_qty}

            if product_choice:
                self.cart[product_id]['product_choice'] = product_choice

            if product.discounted_price:
                self.cart[product_id]['discounted_price'] = \
                    str(product.discounted_price)

        self.session.modified = True

    def delete(self, product):
        """
        Delete a product from the shopping cart.

        Args:
            product (str or Product): The product or product ID to be deleted.

        Returns:
            None

        Note:
            If the specified product or product ID exists in the cart,
            it will be removed.
            The session will be marked as modified to save the changes.
        """
        self.cart_updated['cart_bool'] = True

        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, qty):
        """
        Update the quantity of a product in the shopping cart.

        Args:
            product (str or Product): The product or product ID to be updated.
            qty (int): The new quantity for the product.

        Returns:
            None

        Note:
            If the specified product or product ID exists in the cart,
            its quantity will be updated.
            The session will be marked as modified to save the changes.
        """
        self.cart_updated['cart_bool'] = True

        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity

        self.session.modified = True

    def __len__(self):
        """
        Get the total number of items in the shopping cart.

        Returns:
            int: The total number of items in the cart.
        """
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate through the items in the shopping cart,
        providing additional product details.

        Yields:
            dict: A dictionary representing each item in the cart,
            including product details.

        Note:
            This method enhances the basic iteration over the
            cart items by providing additional details
            such as the product name, price, discounted price,
            slug, category, ID, image URL, and options name.
            The resulting dictionary for each item also includes
            the 'total' cost, calculated as the price multiplied
            by the quantity of the item in the cart.
        """
        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        cart = self.cart.copy()

        for product in products:

            cart[str(product.id)]['product'] = {
                'name': product.name,
                'price': str(product.price),
                'discounted_price': str(product.discounted_price)\
                if product.discounted_price else None,
                'slug': product.slug,
                'category': {'slug': product.category.slug,
                             'name': product.category.name},
                'id': product.id,
                'image': {'url': product.image.url, },
                'options_name': product.options_name
            }

        for item in cart.values():
            
            item['total'] = Decimal(item['discounted_price']) * item['qty']\
                    if item.get('discounted_price')\
                    else Decimal(item['price']) * item['qty']
            item['total'] = str(item['total'])

            yield item

    def get_subtotal(self):
        """
        Calculate the subtotal cost for all items in the shopping cart.

        Returns:
            Decimal: The calculated subtotal amount.

        Note:
            This method calculates the subtotal cost by
            summing the cost of each item in the cart.
            The cost is determined by multiplying the
            price of each item by its quantity.
        """
        return sum(Decimal(item['price']) *
                   item['qty'] for item in self.cart.values())

    def get_delivery_cost(self):
        """
        Calculate the delivery cost based on the total
        cost of items in the shopping cart.

        Returns:
            Decimal: The calculated delivery cost.

        Note:
            This method calculates the delivery cost based
            on the total cost of items in the cart.
            The delivery cost is determined by different price ranges:
            - If total cost is less than 10, delivery cost is 5.
            - If total cost is less than 20, delivery cost is 4.
            - If total cost is less than 30, delivery cost is 3.
            - If total cost is less than 40, delivery cost is 2.
            - If total cost is 40 or more, delivery is free (cost is 0).
        """
        total_cost = sum(Decimal(item['price']) *
                         item['qty'] for item in self.cart.values())

        if total_cost < 10:
            delivery = 5
        elif total_cost < 20:
            delivery = 4
        elif total_cost < 30:
            delivery = 3
        elif total_cost < 40:
            delivery = 2
        else:
            delivery = 0

        return delivery

    def get_grand_total(self):
        """
        Calculate the grand total for the shopping cart,
        including delivery cost and discounts.

        Returns:
            Decimal: The grand total amount.

        Note:
            This method calculates the grand total by adding
            the delivery cost and subtotal,
            then deducting any applicable discounts.
            If there are no items in the cart, the grand total is set to 0.
        """
        delivery = self.get_delivery_cost()
        total = self.get_subtotal()
        total = delivery + total
        discount = self.get_discounted_total()

        if discount:
            total = total - discount

        if len(self) == 0:
            total = 0

        return total

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()[:16]

    def get_order_num(self):
        """
        Get the unique order number associated with the shopping cart.

        Returns:
            str: The unique order number.

        Note:
            This method returns the unique order number
            generated for the shopping cart.
            The order number is created using a random, unique UUID.
        """
        return self.order_num

    def get_discounted_total(self):
        """
        Calculate the total discount for all
        discounted items in the shopping cart.

        Returns:
            Decimal or None: The total discount amount if
            there are discounted items, else None.

        Note:
            This method calculates the total discount by summing the
            difference between the original price
            and the discounted price for each item in the cart that
            has a 'discounted_price' key.
            If there are no discounted items, the method returns None.
        """
        total_discount = sum(
            (Decimal(item['price']) -
             Decimal(item['discounted_price'])) * item['qty']
            for item in self.cart.values() if item.get('discounted_price',
                                                       False)
        )
        return total_discount if total_discount else 0

    def clear_cart(self):
        """
        Clear all items from the shopping cart.

        Note:
            This method removes all items from the cart by
            setting the 'cart' key in the session to an empty dictionary.
            After clearing the cart, the session is marked
            as modified to save the changes.
        """
        self.session['cart'] = {}
        self.session.modified = True

    def get_cart_status(self):
        """
        Get the status of the shopping cart update.

        Returns:
            bool: The current status of the cart update.

        Note:
            The method returns the current value of
            'cart_bool' from the 'cart_updated' dictionary,
            which indicates whether the shopping cart has been updated.
            After retrieving the status, the 'cart_bool' is reset to False,
            and the session is marked as modified to save the changes.
        """
        status = self.cart_updated['cart_bool']
        self.cart_updated['cart_bool'] = False
        self.session.modified = True
        return status


    def get_meta_data(self):
        cart = self.cart.copy()
        meta_data = {}
        for product_id, item in cart.items():
            meta_data[product_id] = {
                'qty': item['qty'],
                'discounted_price': item['discounted_price']
                if item.get('discounted_price') else None,
                'price': item['price'],
                'total': item['price'] * item['qty']
            }
        return meta_data

