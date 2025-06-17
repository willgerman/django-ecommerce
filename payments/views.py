import os
from typing import Any

from django import http
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import stripe
import json

from products import models as product_models
from cart import models as cart_models
from cart import utils as cart_utils
from payments import utils

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart = cart_models.Cart.objects.get(request)
        items = cart_models.CartItem.objects.filter(cart=cart)

        if items.count() == 0:
            redirect("cart:cart")

        line_items = cart.create_stripe_line_items()

        # customer = account_utils.get_stripe_customer_object(request)

        # if customer:
        #     checkout_session = utils.create_stripe_customer_session(
        #         customer,
        #         line_items,
        #         free_shipping,
        #         cart.shipping_fee,
        #         str(cart.id)
        #     )
        # else:
        #     checkout_session = utils.create_stripe_guest_session(
        #         line_items, 
        #         free_shipping, 
        #         cart.shipping_fee, 
        #         str(cart.id)
        #     )

        checkout_session = utils.create_stripe_guest_session(
            line_items, 
            cart.shipping_fee,
            str(cart.id)
        )

        if not checkout_session:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("cart:cart")

        print(checkout_session.id)

        cart.checkout_session_id = checkout_session.id
        cart.session_id_has_been_checked = False
        cart.save()


        return redirect(checkout_session.url, code=303)


class RedirectSuccessView(View):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    pass


class PaymentSuccessView(TemplateView):
    template_name = "payments/success.html"

    def get(
        self,
        request: http.HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> http.HttpResponse:

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        # cart = cart_models.Cart.objects.get(self.request)
        # context["total"] = cart.total

        cart_utils.clean_up_cart_session(self.request)

        return context


class PaymentCancelView(TemplateView):
    template_name = "payments/cancel.html"