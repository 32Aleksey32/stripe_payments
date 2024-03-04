import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View, generic

from config.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from payment_system.models import Item, ItemAnOrder, Order
from payment_system.utils import convert_currency, create_session, get_default_currency, get_exchange_rate


class BuyView(View):

    def get(self, request, id) -> JsonResponse:
        stripe.api_key = STRIPE_SECRET_KEY
        item = get_object_or_404(Item, pk=id)
        line_items = [{
            'price_data': {
                'unit_amount': int(item.price * 100),
                'currency': item.currency,
                'product_data': {'name': item.name},
            },
            'quantity': 1,
        }]
        return create_session(request, line_items)


class ListItemView(generic.TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        if self.request.user.is_authenticated:
            context['order'] = Order.objects.filter(user=self.request.user).order_by('-id').first()
        return context


class ItemView(generic.TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['item'] = get_object_or_404(Item, id=self.kwargs['id'])
        context['public_key'] = STRIPE_PUBLIC_KEY
        if self.request.user.is_authenticated:
            context['order'] = Order.objects.filter(user=self.request.user).order_by('-id').first()
        return context


class OrderView(generic.TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['order'] = Order.objects.filter(user=self.request.user).order_by('-id').first()
        context['items'] = ItemAnOrder.objects.filter(order_id=self.kwargs['id'])
        context['public_key'] = STRIPE_PUBLIC_KEY
        return context


class ItemAnOrderView(View):

    @method_decorator(login_required)
    def post(self, request) -> HttpResponse:
        if request.user.is_authenticated:
            item_id = request.POST.get('item_id')
            order = Order.objects.filter(user=request.user).order_by('-id').first()
            # Получаем товар в заказе или добавляем товар в заказ
            item_an_order, created = ItemAnOrder.objects.get_or_create(order=order, item_id=item_id)
            # Увеличиваем количество товара, если он уже существует в заказе
            if not created:
                item_an_order.quantity += 1
                item_an_order.save()
                msg = 'Количество товара успешно обновлено в заказе.'
            else:
                msg = 'Товар успешно добавлен в заказ.'
        else:
            msg = 'Необходимо авторизоваться.'
        return HttpResponse(msg)


class PayOrderView(View):

    def get(self, request, id) -> JsonResponse:
        stripe.api_key = STRIPE_SECRET_KEY
        account_default_currency = stripe.Account.retrieve().default_currency
        items = ItemAnOrder.objects.filter(order_id=id)
        default_currency = get_default_currency(items, account_default_currency)

        line_items = []
        for item in items:
            exchange_rate = get_exchange_rate(item.item.currency, default_currency)
            converted_price = convert_currency(item.item.price, exchange_rate)
            line_item = {
                'price_data': {
                    'unit_amount': int(converted_price * 100),
                    'currency': default_currency,
                    'product_data': {'name': item.item.name},
                },
                'quantity': item.quantity
            }
            line_items.append(line_item)

        return create_session(request, line_items)


class SuccessView(View):

    def get(self, request):
        """После успешной оплаты удаляем заказ и создаем новый"""
        if request.user.is_authenticated:
            order = Order.objects.filter(user=request.user).order_by('-id').first()
            order.delete()
            new_order = Order.objects.create(user=request.user)
            result = render(request, 'success.html', {'order': new_order})
        else:
            result = render(request, 'success.html')

        return result


class CancelView(generic.TemplateView):
    template_name = 'cancel.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['order'] = Order.objects.filter(user=self.request.user).order_by('-id').first()
        return context
