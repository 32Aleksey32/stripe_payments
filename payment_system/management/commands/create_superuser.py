from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, **kwargs):
        try:
            User.objects.create_superuser(username='admin', password='admin')
            self.stdout.write(self.style.SUCCESS('Суперпользователь успешно создан.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Ошибка: %s" % e))
