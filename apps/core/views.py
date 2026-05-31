from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView, CreateView
from apps.core.models import Suggestion
from django.contrib import messages
from apps.products.models import Product,ProductCategory,ProductSupplier

#Homepage view
class HomeView(ListView):
    model = Product
    template_name = "core/home.html"
    context_object_name = "products"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        
        if slug:
            # User clicked a category → filter by category
            return Product.objects.filter(product_category__slug=slug)
        else:
            # Homepage default → show products from MPC supplier
            default_supplier = "MPC"   
            return Product.objects.filter(
                product_supplier__supplier_name=default_supplier
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        return context


#Search view        
def search_results(request):
    # Get the search query from the URL
    query = request.GET.get('q')
    products = []

    if query:
        # Search the database where the product 'name' contains the query
        products = Product.objects.filter(product_name__icontains=query)
    
    context = {
        'products': products,
        'query': query
    }
    
    return render(request, 'core/search_results.html', context)


#Product details view(View details in search)
def product_detail(request, slug):
    # Fetch the product using the slug field
    product = get_object_or_404(Product, product_slug=slug)
    
    context = {
        'product': product
    }
    
    return render(request, 'core/product_detail.html', context)

class AboutView(TemplateView):
    template_name = 'core/about.html'

class MixingFormulasView(TemplateView):
    template_name = 'core/mixing_formulas.html'

class FarmingAdvicesView(TemplateView):
    template_name = 'core/farmingadvices.html'

class TipsView(TemplateView):
    template_name = 'core/tips.html'

class ContactView(CreateView):
    model = Suggestion
    template_name = 'core/contacts.html'
    fields = ['name', 'contact_details', 'message']
    success_url = reverse_lazy('contact') #This refresh the page after submission

    def form_valid(self, form):
        #Success message to show the user
        messages.success(self.request, "Thank you! Your message has been received by MPC")
        return super().form_valid(form)
