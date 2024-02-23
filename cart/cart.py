import uuid

from decimal import Decimal

from products.models import Product


class Cart():

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get('cart')
        order_num = self.session.get('order_num')
        cart_updated = self.session.get('cart_updated')

        # New user - generate a new session

        if 'cart' not in request.session:

            cart = self.session['cart'] = { }
            order_num = self.session['order_num'] = str(self._generate_order_number())
            cart_updated = self.session['cart_updated'] = {'cart_bool': False,}

        self.cart = cart
        self.order_num = order_num
        self.cart_updated = cart_updated



    def add(self, product, product_qty, product_choice):
        self.cart_updated['cart_bool'] = True

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty if product_qty > 1 else self.cart[product_id]['qty'] + 1
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

            if product_choice:
                self.cart[product_id]['product_choice'] = product_choice

            if product.discounted_price:
                self.cart[product_id]['discounted_price'] = str(product.discounted_price)

        self.session.modified = True




    def delete(self, product):

        product_id = str(product)

        if product_id in self.cart:

            del self.cart[product_id]

        self.session.modified = True



    def update(self, product, qty):

        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:

            self.cart[product_id]['qty'] = product_quantity

        self.session.modified = True


    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())


    def __iter__(self):
        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        cart = self.cart.copy()

        for product in products:

              cart[str(product.id)]['product'] = {
                'name': product.name,
                'price': float(product.price),
                'discounted_price': product.discounted_price if product.discounted_price else None,
                'slug': product.slug,
                'category': {'slug': product.category.slug, 'name': product.category.name},
                'id': product.id,
                'image': {'url': product.image.url,} 
            }

        for item in cart.values():
            item['price'] = item['price']
            item['total'] = item['price'] * item['qty']

        # Ensure any other Decimal values are converted to float or another JSON-serializable format
            yield item


    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())


    def get_delivery_cost(self):
        total_cost = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

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
        return self.order_num


    def get_discounted_total(self):
        total_discount = sum(
            (Decimal(item['price']) - Decimal(item['discounted_price'])) * item['qty']
            for item in self.cart.values() if item.get('discounted_price', False)
        )
        return total_discount if total_discount else None


    def clear_cart(self):
        self.session['cart'] = {}
        self.session.modified = True


    def get_cart_status(self):
        status = self.cart_updated['cart_bool']
        self.cart_updated['cart_bool'] = False
        self.session.modified = True
        return status



