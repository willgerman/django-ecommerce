from django.urls import path
from .views import CartView, CartUpdateView, CartUpdateQuantityView, CartDeleteView, CartCouponView

app_name = "cart"

urlpatterns = [
    path("cart", CartView.as_view(), name="cart"),
    path("delete/", CartDeleteView.as_view(), name="delete"),
    path("update/", CartUpdateView.as_view(), name="update"),
    path("update-quantity/", CartUpdateQuantityView.as_view(), name="update-quantity"),
    path("coupon/", CartCouponView.as_view(), name="coupon"),
]