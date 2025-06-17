from django.urls import path

from . import views
from .views import SearchView

app_name = "search"

urlpatterns = [
    path("", SearchView.as_view(), name="search"),
]