# API Gateway Documentation

## Единый API для электронного магазина

API Gateway обеспечивает единую точку входа для фронтенда, скрывая внутреннюю микросервисную архитектуру.

**Base URL**: `http://localhost:8000`

---

## 🔐 Авторизация

Единый админский ключ для всех операций администрирования:
```
Authorization: Bearer admin_master_key_2024
```

---

## 📦 Products API (Каталог товаров)

### Публичные эндпоинты:

#### GET /api/products - Получить товары с фильтрами
```bash
GET /api/products?product_type=телефон&brand=Apple&price_min=50000&price_max=150000&limit=20
```

#### GET /api/products/{id} - Получить товар по ID
```bash
GET /api/products/123e4567-e89b-12d3-a456-426614174000
```

### Админские эндпоинты:

#### POST /api/products - Создать товар
```bash
POST /api/products
Authorization: Bearer admin_master_key_2024
Content-Type: application/json

{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "iPhone 15 Pro",
    "category_id": 1,
    "description": "Latest iPhone with advanced features",
    "characteristics": {
        "type": "телефон",
        "brand": "Apple",
        "color": "черный",
        "memory": "128GB"
    },
    "created_at": "2024-01-01T00:00:00",
    "amount": 10,
    "price": 99999.0
}
```

#### PATCH /api/products/{id} - Обновить товар
```bash
PATCH /api/products/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer admin_master_key_2024
Content-Type: application/json

{
    "price": 89999.0,
    "amount": 15
}
```

#### DELETE /api/products/{id} - Удалить товар
```bash
DELETE /api/products/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer admin_master_key_2024
```

---

## 🛒 Orders API (Управление заказами)

### Публичные эндпоинты:

#### POST /api/orders - Создать заказ
```bash
POST /api/orders
Content-Type: application/json

{
    "product_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### GET /api/orders/{id} - Получить заказ по ID
```bash
GET /api/orders/1
```

#### POST /api/orders/{id}/confirm - Подтвердить заказ
```bash
POST /api/orders/1/confirm
```

### Админские эндпоинты:

#### GET /api/orders - Получить все заказы
```bash
GET /api/orders?limit=50&offset=0
Authorization: Bearer admin_master_key_2024
```

#### PATCH /api/orders/{id} - Обновить статус заказа
```bash
PATCH /api/orders/1
Authorization: Bearer admin_master_key_2024
Content-Type: application/json

{
    "status": "delivered"
}
```

**Доступные статусы:**
- `created` - Создан
- `paid` - Оплачен
- `shipped` - Отправлен
- `in_transit` - В пути
- `delivered` - Доставлен
- `cancelled` - Отменен

---

## 🔧 Системные эндпоинты

### GET /health - Проверка здоровья
```bash
GET /health
```
**Response:** `Gateway is healthy`

---

## 🚀 Запуск системы

### Полный запуск всех сервисов:
```bash
# Создать общую сеть
docker network create app-shared-network

# Запустить всю систему
docker-compose -f docker-compose.main.yml up -d
```

### Поэтапный запуск:
```bash
# 1. Создать сеть
docker network create app-shared-network

# 2. Запустить RabbitMQ
cd rabbitmq && docker-compose up -d && cd ..

# 3. Запустить Order Service (с PostgreSQL)
cd order_service && docker-compose up -d && cd ..

# 4. Запустить Catalog Service (с Elasticsearch и Redis)
cd catalog_service && docker-compose up -d && cd ..

# 5. Запустить Notification Service
cd notification-service && docker-compose up -d && cd ..

# 6. Запустить API Gateway
cd api_gateway && docker-compose up -d && cd ..
```

---

## 🌐 CORS настройки

Gateway автоматически добавляет CORS заголовки:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Authorization, Content-Type, ...`

---

## 📊 Мониторинг и логирование

### Логи Gateway:
```bash
docker logs api-gateway -f
```

### Логи сервисов:
```bash
docker logs catalog-service-api -f
docker logs order-service-api -f
docker logs notification-service -f
```

### Health checks:
```bash
# Gateway health
curl http://localhost:8000/health

# Catalog service (через gateway)
curl http://localhost:8000/api/products

# Order service (через gateway)
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": "123e4567-e89b-12d3-a456-426614174000"}'
```

---

## 🔒 Безопасность

### Единый админский ключ
Все админские операции используют один ключ: `admin_master_key_2024`

### Настройка в .env файлах:
```env
# catalog_service/.env
admin_api_key=admin_master_key_2024

# order_service/.env  
admin_api_key=admin_master_key_2024
```

### Валидация на уровне сервисов:
- Каждый сервис самостоятельно проверяет Authorization header
- Gateway только маршрутизирует запросы
- Ошибки авторизации возвращают 401 Unauthorized

---

## 📱 Примеры для фронтенда

### Получение товаров:
```javascript
const response = await fetch('http://localhost:8000/api/products?limit=20');
const products = await response.json();
```

### Создание заказа:
```javascript
const order = await fetch('http://localhost:8000/api/orders', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        product_id: 'product-uuid-here'
    })
});
```

### Админские операции:
```javascript
const adminHeaders = {
    'Authorization': 'Bearer admin_master_key_2024',
    'Content-Type': 'application/json'
};

// Создать товар
await fetch('http://localhost:8000/api/products', {
    method: 'POST',
    headers: adminHeaders,
    body: JSON.stringify(productData)
});

// Получить все заказы
const orders = await fetch('http://localhost:8000/api/orders', {
    headers: adminHeaders
});
```

---

## 🏗️ Архитектура

```
Frontend (React/Vue/Angular)
       ↓
API Gateway (Nginx) :8000
       ↓
┌─────────────────┬─────────────────┐
│ Catalog Service │  Order Service  │
│     :8000       │     :8080       │
│                 │                 │
│ - Elasticsearch │ - PostgreSQL    │
│ - Redis         │ - RabbitMQ      │
└─────────────────┴─────────────────┘
                  ↓
          Notification Service
               ↓
           Telegram API
```

Фронтенд видит только Gateway на порту 8000 и работает с ним как с единым API сервисом.