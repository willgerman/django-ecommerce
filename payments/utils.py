import requests
from django.conf import settings

# from django.core.files.base import ContentFile
# from django.core.mail import EmailMessage, send_mail

from decimal import Decimal

import stripe

from accounts import models as account_models
from products import models as product_models

# temporary domain_url configuration
DOMAIN_URL = "http://127.0.0.1:8000/"

"""
Create "Buy Now" line item.
"""
def create_buynow_line_items(
    product: product_models.Product,
    quantity: int,
) -> list:
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product.name,
                    "images": [product.image],
                },
                "unit_amount_decimal": product.default_price * 100,
            },
            "quantity": quantity,
        }
    ]

    return line_items


"""
Get shipping data
"""
def get_shipping_option(shipping_fee: Decimal):
    shipping_fee = int(shipping_fee * 100)

    shipping_options = [
        {
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {
                    "amount": shipping_fee,
                    "currency": "usd"
                },
                "display_name": "Standard Shipping & Handling",
                "delivery_estimate": {
                    "minimum": {
                        "unit": "business_day", "value": 3
                    },
                    "maximum": {
                        "unit": "business_day", "value": 7
                    }
                },
            }
        }
    ]

    return shipping_options

"""
"""
def create_stripe_guest_session(
    line_items: list,
    shipping_fee: Decimal,
    cart_id: str,
    success_url: str = "success",
    cancel_url: str = "cancel",
) -> stripe.checkout.Session:

    success_url = DOMAIN_URL + success_url
    cancel_url = DOMAIN_URL + cancel_url

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            automatic_tax={"enabled": True},
            mode="payment",
            shipping_address_collection={"allowed_countries": ["US"]},
            shipping_options=get_shipping_option(shipping_fee),
            invoice_creation={"enabled": True},
            client_reference_id=cart_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return checkout_session
    except Exception as e:
        print("An exception has occurred: {}".format(e))
        return None
