import csv

from django.core.management.base import BaseCommand

from config.settings import BASE_DIR
from payment_system.models import Item


class Command(BaseCommand):
    help = 'Добавление товаров в БД'

    def handle(self, **kwargs):
        file = f'{BASE_DIR}/payment_system/management/items.csv'
        try:
            with open(file, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    Item.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        price=row[3],
                        currency=row[4]
                    )
            self.stdout.write(self.style.SUCCESS('Товары успешно добавлены в БД.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Ошибка: %s" % e))
