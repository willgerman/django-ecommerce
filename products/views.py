from django.db.models.query import QuerySet

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, ProductImage, Category


class ProductListView(ListView):
    model = Product  
    template_name = 'products/listings.html'

    def get_queryset(self) -> QuerySet[any]:
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        queryset = self.model.objects.filter(category_id=self.category.id, is_published=True)

        return queryset.order_by('date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self.category
        context['products'] = Product.objects.filter(category=self.category, is_published=True)

        return context

class ProductDetailView(DetailView):
    model = Product  
    template_name = 'products/details.html'

    def get_object(self):
        return get_object_or_404(
            Product,
            category__slug=self.kwargs['category'],
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        context['product'] = product
        
        return context