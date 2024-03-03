from django.contrib import admin

from .models import Item, ItemAnOrder, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price_an_order')


@admin.register(ItemAnOrder)
class ItemAnOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'total_price', 'currency')
    search_fields = ('item',)

    def save_model(self, request, obj, form, change):
        # Проверяем, существует ли уже запись с данным товаром в заказе
        item_an_order = ItemAnOrder.objects.filter(order=obj.order, item=obj.item).first()
        if item_an_order:
            # Если запись уже существует, увеличиваем количество
            item_an_order.quantity += obj.quantity
            item_an_order.save()
            return
        super().save_model(request, obj, form, change)
