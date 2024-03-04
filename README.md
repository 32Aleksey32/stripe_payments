## Как запустить проект:

1. **Клонируйте репозиторий на свой компьютер.**
```
git clone https://github.com/32Aleksey32/stripe_payments.git
```

2. **Зарегистрируйтесь на сайте Stripe:**

    Перейдите на https://stripe.com и зарегистрируйтесь. Получите Publishable key и Secret key.


3. **Создайте .env файл, с параметрами:**
```
STRIPE_PUBLIC_KEY=<Publishable key с сайта stripe.com>
STRIPE_SECRET_KEY=<Secret key с сайта stripe.com>
SECRET_KEY=<любой набор символов>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя бд>
POSTGRES_USER=<пользователь бд>
POSTGRES_PASSWORD=<пароль бд>
DB_HOST=db
DB_PORT=5432
```

4. **Запустите процесс создания и запуск контейнеров:**
```
docker-compose up
```

5. **Перейдите на страницу http://localhost:8000**


### Описание:
Проект позволяет оформить заказ с использованием платежной системы Stripe.

**Для оформления заказа или покупки товара:**

1. Перейдите на главную страницу.
2. Нажмите кнопку "Купить" или "Добавить в заказ", затем нажмите "Оплатить заказ".

*(Примечание: неавторизованным пользователям недоступна кнопка "Добавить в заказ". Чтобы она появилась,
необходимо войти в админку под нужным пользователем. При создании нового пользователя автоматически создается заказ.
После успешного оформления заказа предыдущий заказ удаляется и автоматически создается новый.)*

**Валюты товаров:**

- Каждый товар имеет свою валюту.
- При оплате одного товара платежная система предложит оплатить в той валюте, которая указана для этого товара.
- При добавлении в заказ разных товаров в одной и той же валюте, платежная система оплатит в этой же валюте.
- Если товары в заказе имеют разную валюту, платежная система предложит оплатить заказ в валюте, указанной по умолчанию в настройках Вашего аккаунта Stripe.

Для тестирования платежей используйте следующие номера карт:

- **4242 4242 4242 4242** -- Завершается успешно и платеж обрабатывается немедленно.
- **4000 0000 0000 3220** -- Для успешного платежа требуется аутентификация 3D Secure 2.
- **4000 0000 0000 9995** -- Кредитная карта будет отклонена, так как на карте недостаточно средств.


### Доступные страницы:
- Получение Stripe Session Id:
  ```
  GET /buy/{id}/
  ```

- Получение данных о товаре:
  ```
  GET /item/{id}/
  ```

- Добавление товара в заказ:
  ```
  POST /add_to_order/
  ```

- Просмотр заказа и товаров в нем:
  ```
  GET /order/{id}/
  ```

- Оплата заказа:
  ```
  GET /order/{id}/pay_order/
  ```

### Стек технологий использованный в проекте:
- Python 3.10
- Django 5.0.2
- stripe 8.4.0
- Docker
- PostgreSQL