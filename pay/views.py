import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Item, Order

# Ключи для разных валют
STRIPE_KEYS = {
    'usd': {
        'public': settings.STRIPE_PUBLIC_KEY_USD,
        'secret': settings.STRIPE_SECRET_KEY_USD
    },
    'eur': {
        'public': settings.STRIPE_PUBLIC_KEY_EUR,
        'secret': settings.STRIPE_SECRET_KEY_EUR
    }
}

def get_stripe_keys(currency):
    return STRIPE_KEYS.get(currency, STRIPE_KEYS['usd'])

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_keys = get_stripe_keys(item.currency)
    return render(request, 'dj/item.html', {
        'item': item, 
        'STRIPE_PUBLIC_KEY': stripe_keys['public']
    })

def create_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_keys = get_stripe_keys(item.currency)
    stripe.api_key = stripe_keys['secret']
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    # Используем валюту первого товара в заказе или USD по умолчанию
    currency = 'usd'
    if order.items.exists():
        currency = order.items.first().currency
    
    stripe_keys = get_stripe_keys(currency)
    return render(request, 'dj/order.html', {
        'order': order, 
        'STRIPE_PUBLIC_KEY': stripe_keys['public'],
        'currency': currency
    })

def create_order_checkout_session(request, id):
    order = get_object_or_404(Order, id=id)
    
    # Определяем валюту (берем первую из заказа)
    currency = 'usd'
    if order.items.exists():
        currency = order.items.first().currency
    
    stripe_keys = get_stripe_keys(currency)
    stripe.api_key = stripe_keys['secret']
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': f'Order #{order.id}',
                },
                'unit_amount': order.total_price_cents(),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})


def create_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_keys = get_stripe_keys(item.currency)
    stripe.api_key = stripe_keys['secret']
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            metadata={
                'item_id': item.id,
                'item_name': item.name
            }
        )
        return JsonResponse({
            'client_secret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def item_detail_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_keys = get_stripe_keys(item.currency)
    return render(request, 'dj/item_payment_intent.html', {
        'item': item, 
        'STRIPE_PUBLIC_KEY': stripe_keys['public']
    })