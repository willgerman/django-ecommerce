from django.urls import path

from .views import ContactView

app_name = "support"

urlpatterns = [
    path("contact", ContactView.as_view(), name="contact"),
    path('contact/', ContactView.as_view(), name='support'), 
]