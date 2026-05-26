from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # The URL to view your new control panel template
    path('', views.order_page, name='order_page'), 
    
    # The URL we just fixed for the checkout logic
    path('submit/', views.order_submit, name='order_submit'),
]
