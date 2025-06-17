
from django.urls import path

from .views import CreateCheckoutSessionView, PaymentSuccessView, PaymentCancelView

urlpatterns = [
    path(
        'create-checkout-session/',
        CreateCheckoutSessionView.as_view(),
        name='create-checkout-session',
    ),
    path('success', PaymentSuccessView.as_view(), name="success"),
    path('cancel', PaymentCancelView.as_view(), name="cancel")
]