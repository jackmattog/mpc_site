from django.db import models
from typing import Any # Help with VS Code type hinting

class Order(models.Model):
    # --- Type Hints for VS Code (Pylance) ---
    id: int
    items: Any 
    # ----------------------------------------

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent to WhatsApp'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    delivery_location = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Pointing explicitly to the 'products' app's 'Product' model:
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.product_name}"
    
    def get_cost(self):
        return self.price * self.quantity