from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.base import TemplateView

from organization import models as organization_models
from products import models as product_models

# Create your views here.
class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = organization_models.Category.objects.all()

        return context

class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context