from django import http

from cart import models as cart_models
from products import models as product_models

# from django.core.mail import send_mail


"""
Fetch new cart session. If one does not exist, create a new
cart session for the user.
"""
def get_cart_session(request: http.HttpRequest) -> cart_models.Cart:
    cart = cart_models.Cart.objects.get(request)

    # check if returned value is valid (i.e., not None)
    if cart is None:
        cart = new_cart_session(request)

    # if so return cart
    return cart


"""
Create a new cart session for the user and return the created object.
"""
def new_cart_session(request: http.HttpRequest) -> cart_models.Cart:
    cart = cart_models.Cart.objects.new(request, request.user)
    return cart


"""
Determine the total number of items that are present in the cart session.
"""
def get_cart_quantity(cart: cart_models.Cart) -> int:
    items = cart_models.CartItem.objects.filter(cart=cart)

    quantity = 0

    for item in items:
        quantity += item.quantity

    return quantity


"""
Determine the next url that the user will be redirected to.
"""
def get_next_url(next_url: str) -> str:
    if next_url is None or next_url == "":
        next_url = "carts:cart"

    return next_url

"""
Update the contents within the cart session.
"""
def update_cart(
    cart: cart_models.Cart, 
    product: product_models.Product, 
    quantity: int):

        # get the cart item that is added
        cart_item = cart_models.CartItem.objects.filter(
            cart=cart, product_uuid=product.id
        )

        # if the cart_item exists, update the cart
        if cart_item.exists():
            cart_item = cart_item.first()
            cart_item.quantity += int(quantity)
            cart_item.line_total = product.price * int(cart_item.quantity)
            cart_item.save()
        # create a new cart_item if this one does not exist
        else:
            cart_item = cart_models.CartItem.objects.create(
                cart=cart,
                product_uuid=product.id,
                product_object=product,
                name=product.name,
                slug=product.slug,
                image=product.image.url,
                quantity=quantity,
                price=product.price,
                line_total=product.price * int(quantity),
            )

        # if the cart item is already present in the cart, do not update the quantity if it is going to be go over 10



"""
Reset cart session following a completed purchase.
"""
def clean_up_cart_session(request: http.HttpRequest):
    """
    Clean up cart session variables.
    """
    request.session["cart_id"] = None
    request.session["cart_item_count"] = 0


# update_products_stock