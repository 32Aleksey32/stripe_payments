from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import CASCADE, CharField, DecimalField, ForeignKey, ManyToManyField, Model, PositiveIntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver

CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RUB', 'RUB'),
)


class Item(Model):
    name = CharField(unique=True, max_length=100, verbose_name='Наименование')
    description = CharField(max_length=250, default='', blank=True, null=True, verbose_name='Описание')
    price = DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Цена')
    currency = CharField(max_length=3, default='USD', choices=CURRENCY_CHOICES, verbose_name='Валюта')

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'payment_system"."items'

    def __str__(self):
        return f'{self.name}'


class Order(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='user', verbose_name='Пользователь')
    item = ManyToManyField(Item, through='ItemAnOrder', verbose_name='Товар')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'payment_system"."order'

    def __str__(self):
        return f'Заказ № {self.id}'

    @property
    def total_price_an_order(self):
        total = sum(item.total_price for item in self.items.all())
        return f'{total} {self.items.first().currency}' if total else '0.00'
    total_price_an_order.fget.short_description = 'Общая сумма в заказе'


class ItemAnOrder(Model):
    order = ForeignKey(Order, null=True, blank=True, on_delete=CASCADE, related_name='items', verbose_name='Заказ')
    item = ForeignKey(Item, on_delete=CASCADE, verbose_name='Товар')
    quantity = PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        db_table = 'payment_system"."item_an_order'

    @property
    def total_price(self):
        return self.quantity * self.item.price
    total_price.fget.short_description = 'Сумма товара'

    @property
    def currency(self):
        return self.item.currency
    currency.fget.short_description = 'Валюта'


@receiver(post_save, sender=User)
def create_order(sender, instance, created, **kwargs):
    """При создании нового пользователя создается объект Order"""
    if created:
        Order.objects.create(user=instance, id=instance.id)
