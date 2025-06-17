from django.conf import settings
from django.db import models

import uuid

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
import time

import json
from django.core.serializers.json import DjangoJSONEncoder

from discounts.models import Coupon

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def get(self, request):
        # fetch cart object from session data or return NoneType
        cart_id = request.session.get('cart_id', None)

        # strip excess quotes and convert to UUID
        if cart_id is not None:
            cart_id = cart_id.strip('\"')

        # check if the queryset filtered for id returns any objects
        cart_queryset = self.get_queryset().filter(id=cart_id)

        # if an object is found in the queryset, the cart must exist
        if cart_queryset.count() == 1:
            # declare this cart as not new and assign the returned object accordingly
            is_new_cart = False
            cart = cart_queryset.first()

            # if the existing cart session does NOT have an assigned user, and the user is logged in, assign said user to the cart
            if request.user.is_authenticated and cart.user is None:
                cart.user = request.user
                cart.save()
            
            # if there is a cart, return it
            return cart

        # if no cart is found, return none
        return None

    def new(self, request, user=None):
        user_object = None

        if user is not None:
            if user.is_authenticated:
                user_object = user

        # create new cart session
        is_new_cart = True
        cart = self.model.objects.create(user=user_object)

        # save new cart session
        request.session["cart_id"] = json.dumps(cart.id, cls=DjangoJSONEncoder)

        return cart

class Cart(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)
    shipping_fee = models.DecimalField(max_digits=100, decimal_places=2, default=5.00)
    subtotal = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    is_cart = models.BooleanField(default=True)
    checkout_session_id = models.CharField(max_length=255, null=True, blank=True)
    session_id_has_been_checked = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.CASCADE)
    discount_value = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    order_id = models.PositiveIntegerField(default=0)

    objects = CartManager()

    def calculate_total(self):
        subtotal = Decimal("0.00")

        subtotal = self.calculate_cart_subtotal()

        tax_rate = Decimal("0.053")

        self.tax = (subtotal * tax_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        self.total = (
            subtotal + Decimal(self.shipping_fee)
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.save()
        
    def calculate_cart_subtotal(self):
        cart_items = CartItem.objects.filter(cart=self)
        subtotal = Decimal("0.00")

        for item in cart_items:
            subtotal += Decimal(item.line_total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        if self.coupon is not None and self.coupon.is_valid_and_active():
            discount_percentage = Decimal(self.coupon.discount / 100)
            discount = subtotal * discount_percentage
            subtotal = subtotal - discount

            amount_off = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return self.subtotal

    """
    Return dollar value of discount amount.
    """
    def get_discount_value(self):
        cart_items = CartItem.objects.filter(cart=self)
        subtotal = Decimal("0.00")
        discount_value = Decimal("0.00")

        for item in cart_items:
            subtotal += Decimal(item.line_total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        discount_percentage = Decimal(self.coupon.discount / 100)
        discount = subtotal * discount_percentage
        
        self.discount_value = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return self.discount_value

        

    """
    Fetch no-discount-applied cart total.
    """
    def get_original_total(self):
        total = Decimal(0.00)
        items = CartItem.objects.filter(cart=self)
        for item in items:
            total += Decimal(item.get_original_price())
        return total

    """
    Create stripe line item data from cart items.
    """
    def create_stripe_line_items(self) -> list:
        items = CartItem.objects.filter(cart=self)
        line_items = []

        discount = Decimal(0.00)
        if self.coupon is not None and self.coupon.is_valid_and_active():
            count = self.count
            subtotal = self.subtotal
            original_total = self.get_original_total()
            difference = original_total - subtotal
            discount = Decimal(difference / count).quantize(
                Decimal("0.01"), 
                rounding=ROUND_HALF_UP
            )

        for item in items:
            price = Decimal(item.price)
            price = price - discount
            price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            sku = item.product_object.sku
            if sku is None:
                sku = ""
            else:
                sku = " - " + sku

            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name + sku,
                            # "images": [item.image], # this must be updated on a prod environment to show images (i.e., served via CDN)
                        },
                        "unit_amount_decimal": price * 100,
                    },
                    "quantity": item.quantity
                }
            )

        return line_items

    def __str__(self):
        return str(self.id)


class CartItem(models.Model): 
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_uuid = models.UUIDField(
        primary_key = False,
        default = uuid.uuid4,
        editable = True
    )
    product_object = models.ForeignKey("products.Product", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True) 
    image = models.CharField(max_length=520)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    line_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    def get_original_price(self):
        return self.product_object.price * self.quantity

    def __str__(self):
        return str(self.id)