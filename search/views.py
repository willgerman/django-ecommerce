from typing import Any, Dict
from django.views.generic.base import TemplateView

# from .utils import construct_search_context


class SearchView(TemplateView):
    template_name = "search/search.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # qs = self.request.GET
        # context = construct_search_context(qs, context)

        return context

    def construct_search_context(qs, context):
        pass

    def append_query_string(query_string, query_name, query):
        pass