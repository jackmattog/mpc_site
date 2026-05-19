from django.urls import path
from . import views
from .views import HomeView

#App name 
app_name = "core"

urlpatterns = [
    path("",HomeView.as_view(),name="home")
]
