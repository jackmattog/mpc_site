from django.urls import path
from .views import OrderPageView, OrderSubmitView

app_name = 'orders'

urlpatterns = [
    path('checkout/', OrderPageView.as_view(), name='order_page'),
    path('submit/', OrderSubmitView.as_view(), name='order_submit'),
]