from django.urls import path
from . import views
from .views import AboutView, ContactView, FarmingAdvicesView, HomeView, MixingFormulasView, TipsView

#App name 
app_name = "core"

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("category/<slug:slug>/",HomeView.as_view(),name="categories"),
    path("search/",views.search_results,name='search_results'),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("",AboutView.as_view(),name="about"),
    path("",MixingFormulasView.as_view(),name="mixing_formulas"),
    path("",FarmingAdvicesView.as_view(),name="farming_advices"),
    path("",TipsView.as_view(),name="tips"),
    path("",ContactView.as_view(),name="contacts"),

]
