# Order Service API Documentation

## Эндпоинты для работы с заказами

### 1. **POST /api/orders** - Создание заказа

Создает новый заказ для указанного товара и отправляет уведомление в Telegram.

**Request:**
```bash
POST /api/orders
Content-Type: application/json

{
    "product_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response (201):**
```json
{
    "id": 1,
    "product_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "created",
    "amount": 1,
    "price": 0.0,
    "created_at": "2024-01-01T10:00:00",
    "paid_at": null,
    "shipped_at": null,
    "delivered_at": null
}
```

**Error Responses:**
- **400 Bad Request**: Если товар не существует в каталоге
```json
{
    "detail": "Product does not exist in catalog"
}
```

### 2. **GET /api/orders/{id}** - Получение статуса заказа

Возвращает информацию о заказе и его текущем статусе.

**Request:**
```bash
GET /api/orders/1
```

**Response (200):**
```json
{
    "id": 1,
    "product_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "paid",
    "amount": 1,
    "price": 99999.0,
    "created_at": "2024-01-01T10:00:00",
    "paid_at": "2024-01-01T10:15:00",
    "shipped_at": null,
    "delivered_at": null
}
```

**Error Responses:**
- **404 Not Found**: Если заказ не найден
```json
{
    "detail": "Order not found"
}
```

## Статусы заказов

Заказ может находиться в следующих состояниях:

| Статус | Значение | Описание |
|--------|----------|----------|
| `created` | Создан | Заказ создан, но не оплачен |
| `paid` | Оплачен | Заказ оплачен покупателем |
| `shipped` | Отправлен | Заказ передан в службу доставки |
| `in_transit` | В пути | Заказ находится в процессе доставки |
| `delivered` | Доставлен | Заказ успешно доставлен |
| `cancelled` | Отменен | Заказ отменен |

## Уведомления в Telegram

При создании заказа автоматически отправляется уведомление в Telegram чат.

### Настройка Telegram уведомлений

1. **Создайте Telegram бота:**
   - Напишите @BotFather в Telegram
   - Создайте нового бота командой `/newbot`
   - Получите токен бота

2. **Получите ID чата:**
   - Добавьте бота в нужный чат или группу
   - Отправьте любое сообщение в чат
   - Получите chat_id через API: `https://api.telegram.org/bot{BOT_TOKEN}/getUpdates`

3. **Настройте переменные окружения:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Пример уведомления:
```
Новый заказ создан! ID: 1, Товар: 123e4567-e89b-12d3-a456-426614174000
```

## Существующие эндпоинты (совместимость)

### POST /api/orders/{id}/confirm - Подтверждение заказа

**Request:**
```bash
POST /api/orders/1/confirm
```

**Response (200):**
```json
{
    "id": 1,
    "product_id": "123e4567-e89b-12d3-a456-426614174000", 
    "status": "paid",
    "amount": 1,
    "price": 0.0,
    "created_at": "2024-01-01T10:00:00",
    "paid_at": "2024-01-01T10:15:00",
    "shipped_at": null,
    "delivered_at": null
}
```

При подтверждении заказа также отправляется Telegram уведомление:
```
Заказ #1 оплачен!
```

## Интеграция с Catalog Service

Order Service проверяет существование товара в Catalog Service перед созданием заказа через HTTP API:
- URL каталога: `http://catalog-service-api:8000`
- Эндпоинт проверки: `/api/products/{product_id}`

## Интеграция с RabbitMQ

Уведомления отправляются через RabbitMQ в очередь `rabbitmq_notifications_queue`, которую обрабатывает Notification Service.

**Конфигурация RabbitMQ:**
```env
RABBITMQ_HOST=rabbit
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_NOTIFICATIONS_QUEUE=rabbitmq_notifications_queue
```

## База данных

Order Service использует PostgreSQL для хранения заказов:

**Таблица `orders`:**
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'created',
    amount INTEGER NOT NULL,
    price FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    paid_at TIMESTAMP NULL,
    shipped_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL
);
```

## Curl примеры

### Создание заказа
```bash
curl -X POST "http://localhost:8080/api/orders" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "123e4567-e89b-12d3-a456-426614174000"}'
```

### Получение информации о заказе  
```bash
curl -X GET "http://localhost:8080/api/orders/1"
```

### Подтверждение заказа
```bash
curl -X POST "http://localhost:8080/api/orders/1/confirm"
```