from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic

from cart import models as cart_models
from cart import utils as cart_utils
from products import models as product_models
from discounts import models as discount_models


class CartView(generic.TemplateView):
    template_name = "carts/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cart_id = self.request.session.get("cart_id")

        if cart_id is None:
            return context

        cart = cart_models.Cart.objects.get(self.request)
        items = cart_models.CartItem.objects.filter(cart=cart)

        context["cart"] = cart
        context["cart_items"] = items

        # if self.coupon is not None and self.coupon.is_valid_and_active():
        #     context["amount_off"] = self.get_amount_off()        

        return context
    

class CartUpdateView(generic.View):
    def post(self, request, *args, **kwargs):
        # fetch form data
        form_data = request.POST

        product_id = form_data.get("product_id")
        quantity = form_data.get("product_quantity")

        # fetch current path from form_data
        next_url = request.POST.get("next_url")

        # check path & update if necessary
        next_url = cart_utils.get_next_url(next_url)

        # check if product exists and has a valid quantity
        if product_id is None or quantity is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        # check to see if user attempted to commit quantity fraud
        if int(quantity) < 0 or int(quantity) > 10:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        # get product object from databsae
        product = None

        try:
            product = product_models.Product.objects.get(id=product_id)
        except product_models.Product.DoesNotExist:
            messages.error(request, "Item not found.")
            return redirect(next_url)

        # get which action the user attempted to take
        user_action = form_data.get("user_action")

        # cannot fetch user_action, throw error
        if user_action is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        # get existing cart session, or create a new one. always returns a cart session
        cart = cart_utils.get_cart_session(request)

        if user_action == "buy_now":
            next_url = "cart:cart"

        # update cart with new item(s)
        cart_utils.update_cart(cart, product, quantity)

        # update cart count & save in session
        cart.count = cart_utils.get_cart_quantity(cart)
        
        # get cart subtotal, and total
        cart.calculate_total()
        cart.save()

        request.session["cart_item_count"] = cart.count

        messages.success(request, "Item added to your cart.")

        return redirect(next_url)


class CartUpdateQuantityView(generic.View):
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        user_action = form_data.get("action")
        next_url = "cart:cart"

        if user_action is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        product_id = form_data.get("cart_item_id")

        if product_id is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        cart = cart_models.Cart.objects.get(request)

        if cart is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        cart_item = cart_models.CartItem.objects.filter(
            id=product_id,
            cart=cart
        )

        if cart_item.exists():
            cart_item = cart_item.first()

        if user_action == "increment":
            cart_item.quantity += 1

            if cart_item.quantity > 10:
                messages.error(request, "Item has a max quantity of 10 per order.")
                return redirect(next_url)

        if user_action == "decrement":
            cart_item.quantity -= 1

            if cart_item.quantity < 1:
                messages.error(request, "Item has a minimum quantity of 1.")
                return redirect(next_url)

        cart_item.line_total = cart_item.quantity * cart_item.price
        cart_item.save()

        cart.count = cart_utils.get_cart_quantity(cart)
        cart.calculate_total()
        cart.save()
    
        request.session["cart_item_count"] = cart.count

        return redirect(next_url)


class CartDeleteView(generic.View):
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        user_action = form_data.get("action")
        next_url = "cart:cart"

        if user_action is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        product_id = form_data.get("cart_item_id")

        if product_id is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        cart = cart_models.Cart.objects.get(request)

        if cart is None:
            messages.error(request, "Internal server error, please try again.")
            return redirect(next_url)

        cart_item = cart_models.CartItem.objects.filter(
            id=product_id,
            cart=cart
        )

        if user_action == "delete":
            cart_item.delete()

        messages.success(request, "Item removed from cart.")

        cart.count = cart_utils.get_cart_quantity(cart)
        cart.calculate_total()
        cart.save()

        request.session["cart_item_count"] = cart.count

        return redirect(next_url)


class CartCouponView(generic.View):
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        code = form_data.get("coupon_code").upper()

        lookup = discount_models.Coupon.objects.filter(
            code=code,
            is_active=True
        )

        if lookup.first() is not None and lookup.first().is_valid_and_active():
            cart = cart_models.Cart.objects.get(request)
            cart.coupon = lookup.first()
            cart.discount_value = cart.get_discount_value()
            cart.calculate_total()
            cart.save()
            return redirect("cart:cart")

        messages.error(request, "Invalid coupon code.")

        return redirect("cart:cart")