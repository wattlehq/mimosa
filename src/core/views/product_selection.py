import json
import stripe
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from core.models.order import OrderSession, OrderSessionLine
from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.property import Property

# Fetch certificates from Stripe Product Catalogue

# stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# def get_stripe_products():
#     products = stripe.Product.list(active=True)
#     for product in products:
#         if product.default_price:
#             price = stripe.Price.retrieve(product.default_price)
#             product.price = price.unit_amount / 100
#         else:
#             product.price = None
#     return products

# def product_selection(request):
#     stripe_products = get_stripe_products()
#     context = {
#         'stripe_products': stripe_products
#     }
#     return render(request, 'pages/product_selection.html', context)

def product_selection(request):
    certificates = Certificate.objects.all()
    fees = Fee.objects.all()
    context = {
        'certificates': certificates,
        'fees': fees
    }
    return render(request, 'pages/product_selection.html', context)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_items = data.get('selectedItems', [])
        
        line_items = []
        for item in selected_items:
            line_items.append({
                'price_data': {
                    'currency': 'aud',
                    'unit_amount': int(item['price'] * 100),  # Stripe expects amount in cents
                    'product_data': {
                        'name': item['name'],
                    },
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        )
        
        return JsonResponse({'url': checkout_session.url})
    return JsonResponse({'error': 'Invalid request method'})

def payment_success(request):
    return render(request, 'pages/payment_success.html')

def payment_cancel(request):
    return render(request, 'pages/payment_cancel.html')