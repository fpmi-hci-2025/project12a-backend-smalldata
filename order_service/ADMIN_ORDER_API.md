# Admin Order Management API

## Админские эндпоинты для управления заказами

Все админские эндпоинты требуют авторизацию через header:
```
Authorization: Bearer super_secret_admin_orders_key_2024
```

---

## 1. **GET /api/orders** - Получить все заказы

Возвращает список всех заказов с пагинацией (только для администратора).

### Request:
```bash
GET /api/orders?limit=50&offset=0
Authorization: Bearer super_secret_admin_orders_key_2024
```

### Query Parameters:
- `limit` (optional): Количество заказов на странице (макс. 1000, по умолчанию 100)
- `offset` (optional): Смещение для пагинации (по умолчанию 0)

### Response (200):
```json
{
    "orders": [
        {
            "id": 1,
            "product_id": "123e4567-e89b-12d3-a456-426614174000",
            "status": "delivered",
            "amount": 1,
            "price": 99999.0,
            "created_at": "2024-01-01T10:00:00",
            "paid_at": "2024-01-01T10:15:00",
            "shipped_at": "2024-01-01T11:00:00",
            "delivered_at": "2024-01-02T14:30:00"
        },
        {
            "id": 2,
            "product_id": "456e7890-e12b-34c5-d678-901234567890",
            "status": "paid",
            "amount": 2,
            "price": 159999.0,
            "created_at": "2024-01-02T09:30:00",
            "paid_at": "2024-01-02T09:45:00",
            "shipped_at": null,
            "delivered_at": null
        }
    ],
    "total": 2,
    "limit": 100,
    "offset": 0
}
```

---

## 2. **PATCH /api/orders/{id}** - Обновить статус заказа

Обновляет статус указанного заказа и отправляет уведомление в Telegram.

### Request:
```bash
PATCH /api/orders/1
Authorization: Bearer super_secret_admin_orders_key_2024
Content-Type: application/json

{
    "status": "delivered"
}
```

### Доступные статусы:
- `"created"` - Создан
- `"paid"` - Оплачен  
- `"shipped"` - Отправлен
- `"in_transit"` - В пути
- `"delivered"` - Доставлен
- `"cancelled"` - Отменен

### Response (200):
```json
{
    "id": 1,
    "product_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "delivered",
    "amount": 1,
    "price": 99999.0,
    "created_at": "2024-01-01T10:00:00",
    "paid_at": "2024-01-01T10:15:00",
    "shipped_at": "2024-01-01T11:00:00",
    "delivered_at": "2024-01-02T14:30:00"
}
```

### Автоматическое обновление временных меток:
- При изменении статуса на `"paid"` → устанавливается `paid_at`
- При изменении статуса на `"shipped"` → устанавливается `shipped_at`  
- При изменении статуса на `"delivered"` → устанавливается `delivered_at`

---

## Уведомления в Telegram

При изменении статуса заказа автоматически отправляются уведомления:

- **paid**: "Заказ #1 оплачен!"
- **shipped**: "Заказ #1 отправлен!"
- **in_transit**: "Заказ #1 в пути!"
- **delivered**: "Заказ #1 доставлен!"
- **cancelled**: "Заказ #1 отменен!"

---

## Обработка ошибок

### 401 Unauthorized - Неверный API ключ:
```json
{
    "detail": "Invalid or missing admin API token"
}
```

### 404 Not Found - Заказ не найден:
```json
{
    "detail": "Order not found"
}
```

### 400 Bad Request - Неверный статус:
```json
{
    "detail": "Invalid status value"
}
```

---

## Curl примеры

### Получить все заказы (первые 20):
```bash
curl -X GET "http://localhost:8080/api/orders?limit=20&offset=0" \
  -H "Authorization: Bearer super_secret_admin_orders_key_2024"
```

### Отметить заказ как отправленный:
```bash
curl -X PATCH "http://localhost:8080/api/orders/1" \
  -H "Authorization: Bearer super_secret_admin_orders_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

### Отметить заказ как доставленный:
```bash
curl -X PATCH "http://localhost:8080/api/orders/1" \
  -H "Authorization: Bearer super_secret_admin_orders_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered"}'
```

### Отменить заказ:
```bash
curl -X PATCH "http://localhost:8080/api/orders/1" \
  -H "Authorization: Bearer super_secret_admin_orders_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"status": "cancelled"}'
```

---

## Конфигурация

Добавьте админский API ключ в `.env` файл order_service:

```env
admin_api_key=super_secret_admin_orders_key_2024
```

## Безопасность

- ✅ Все админские операции требуют валидный API ключ
- ✅ API ключ передается в заголовке, не в URL
- ✅ Четкое разделение прав доступа (обычные пользователи vs админы)
- ✅ Логирование всех изменений статусов через уведомления

## Интеграция с существующими эндпоинтами

Эти админские эндпоинты дополняют существующие:
- `POST /api/orders` - создание заказа (публичный)
- `GET /api/orders/{id}` - получение заказа (публичный)
- `POST /api/orders/{id}/confirm` - подтверждение заказа (публичный)

Все изменения статусов отправляют уведомления в общую Telegram очередь.