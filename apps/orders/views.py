import json
import urllib.parse
from django.http import JsonResponse
from apps.products.models import Product  # Adjust this import path if your app structure is different
from django.shortcuts import render

def order_page(request):
    # Fetch all products to populate the left-side catalog in the template
    products = Product.objects.all()
    
    # Renders the zero-friction checkout template
    return render(request, 'orders/order_page.html', {'products': products})


def order_submit(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON payload from the frontend
            data = json.loads(request.body)
            cart_items = data.get("cart_items", [])
            delivery_location = data.get("delivery_location", "").strip()

            if not delivery_location:
                delivery_location = "Not specified (Call customer to confirm)"

            if not cart_items:
                return JsonResponse(
                    {"status": "error", "message": "Your cart is empty."},
                    status=400,
                )

            # Start building the WhatsApp Text Message layout
            whatsapp_msg = "*🛒 NEW MPC EXPRESS ORDER*\n"
            whatsapp_msg += "───────────────────\n\n"

            grand_total = 0
            # order = Order.objects.create(delivery_location=delivery_location, total=0)

            for item in cart_items:
                # The frontend JS sends the slug inside the 'slug' key
                item_slug = item.get("slug")
                quantity = int(item.get("quantity", 1))

                try:
                    # FIX: Looking up the product strictly using your 'product_slug' column
                    product = Product.objects.get(product_slug=item_slug)
                except Product.DoesNotExist:
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "One of the selected products does not exist in the live database.",
                        },
                        status=404,
                    )

                # Calculate financials using exact model field attributes
                subtotal = product.product_price * quantity
                grand_total += subtotal

                # Append item details directly to the WhatsApp text output string
                unit_label = product.product_unit if product.product_unit else "pcs"
                whatsapp_msg += f"📦 *{product.product_name}*\n"
                whatsapp_msg += f"   Qty: {quantity} {unit_label}\n"
                whatsapp_msg += f"   Price: {product.product_price:,} TZS\n"
                whatsapp_msg += f"   Subtotal: {subtotal:,} TZS\n\n"

                # Optional: Save individual items to your database here if needed
                # OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.product_price)

            # Finish formatting the WhatsApp bill layout
            whatsapp_msg += "───────────────────\n"
            whatsapp_msg += f"💰 *Grand Total:* {grand_total:,} TZS\n"
            whatsapp_msg += f"📍 *Delivery:* {delivery_location}\n\n"
            whatsapp_msg += (
                "⚡ _Please tap send to submit. I am waiting for your call confirmation!_"
            )

            # Clean URL encoding for the WhatsApp string payload
            encoded_msg = urllib.parse.quote(whatsapp_msg)

            # CHANGE THIS: Put your actual business WhatsApp phone number (with country code, no + symbol)
            # Example for Tanzania: "255712345678"
            whatsapp_business_number = "255794700716"

            whatsapp_url = f"https://wa.me/{whatsapp_business_number}?text={encoded_msg}"

            # Optional: Update the order grand total in your database before completing response
            # order.total = grand_total
            # order.save()

            return JsonResponse({"status": "success", "whatsapp_url": whatsapp_url})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data received."},
                status=400,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Server processing error: {str(e)}"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed."}, status=405
    )