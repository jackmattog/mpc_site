from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

#Homepage view
class HomeView(TemplateView):
    template_name = "core/home.html"
