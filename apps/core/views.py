from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from apps.products.models import Product,ProductCategory
# Create your views here.

#Homepage view
class HomeView(ListView):
    model = Product
    template_name = "core/home.html"
    context_object_name = "products"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            return Product.objects.filter(category__slug=slug)
        return Product.objects.all()
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        return context
    