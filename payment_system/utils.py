from typing import List

import requests
import stripe
from django.http import JsonResponse


def create_session(request, line_items: List[dict]) -> JsonResponse:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'session_id': session.id})


def get_default_currency(items, account_default_currency) -> str:
    currencies = set(item.item.currency for item in items)
    if len(currencies) == 1:
        # Если все товары имеют одинаковую валюту, используем эту валюту для оплаты
        default_currency = currencies.pop()
    else:
        # Если хотя бы один товар имеет другую валюту, используем валюту по умолчанию из настроек Stripe
        default_currency = account_default_currency
    return default_currency


def get_exchange_rate(item_currency, default_currency) -> float:
    url = f"https://api.exchangerate-api.com/v4/latest/{item_currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(default_currency.upper())


def convert_currency(amount, exchange_rate) -> float:
    return float(amount) * float(exchange_rate)
