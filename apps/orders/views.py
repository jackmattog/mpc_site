import json
import urllib.parse
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from products.models import Product  # Product model in products app
from .models import Order, OrderItem

class OrderPageView(TemplateView):
    """Renders the main ordering control panel page."""
    template_name = 'orders/order_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching all products to display as options on the checkout page
        context['products'] = Product.objects.all()
        return context

@method_decorator(csrf_exempt, name='dispatch')
class OrderSubmitView(View):
    """Handles submission, creates DB records, and returns the WhatsApp URL."""
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            customer_name = data.get('customer_name')
            phone_number = data.get('phone_number')
            delivery_location = data.get('delivery_location', '')
            cart_items = data.get('cart_items', [])

            # Validation guardrail
            if not customer_name or not phone_number or not cart_items:
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            # 1. Save master Order record to PostgreSQL
            order = Order.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                delivery_location=delivery_location,
                status='Pending'
            )

            # 2. Prepare WhatsApp text structure matching Page 2 blueprint
            message_lines = [
                f"Ordered by: {customer_name}",
                f"Phone no: {phone_number}",
            ]
            if delivery_location:
                message_lines.append(f"Delivery Location: {delivery_location}")
            
            message_lines.append("\n--- Full Order ---")

            total_amount = 0

            # 3. Save each item line to the database and format text string
            for index, item in enumerate(cart_items, 1):
                product_id = item.get('id')
                qty = int(item.get('quantity', 1))
                
                product = Product.objects.get(id=product_id)
                price = product.product_price
                subtotal = price * qty
                total_amount += subtotal

                # Creating specific item record linked to master order
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=qty
                )

                # Format matching: Index. Name - Qty x Price = Subtotal
                # Safely checking for an optional unit field from product model
                unit = getattr(product, 'unit', 'pcs')
                message_lines.append(f"{index}. {product.product_name} - {qty} {unit} x {price:,} = {subtotal:,} TZS")

            message_lines.append(f"\nTotal: {total_amount:,} TZS")
            full_message = "\n".join(message_lines)

            # 4. Generate direct WhatsApp redirection link
            my_whatsapp_number = "255756340467" 
            encoded_message = urllib.parse.quote(full_message)
            whatsapp_url = f"https://wa.me/{my_whatsapp_number}?text={encoded_message}"

            return JsonResponse({'status': 'success', 'whatsapp_url': whatsapp_url})

        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'One of the selected products does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)