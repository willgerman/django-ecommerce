from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("<slug:slug>/", views.ProductListView.as_view(), name='listings'),
    # add category slug to urlconf of details
    path("<slug:category>/<slug:slug>/", views.ProductDetailView.as_view(), name='details'),
]