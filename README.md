# E-commerce Backend - Microservices

Микросервисная архитектура для интернет-магазина электроники с единым API Gateway.

## 🏗️ Архитектура

```
Frontend → API Gateway (Nginx) → Microservices
                                      ↓
┌─────────────────┬─────────────────┬─────────────────┐
│ Catalog Service │  Order Service  │Notification Svc │
│ (Products)      │ (Orders)        │ (Telegram)      │
│                 │                 │                 │
│ - Elasticsearch │ - PostgreSQL    │ - RabbitMQ      │
│ - Redis         │ - RabbitMQ      │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

## 🚀 Быстрый старт

### 1. Настройка переменных окружения
```bash
# Скопировать примеры конфигурации
cp .env.example .env

# Отредактировать .env файл:
# - Установить TELEGRAM_BOT_TOKEN
# - Установить TELEGRAM_CHAT_ID
# - При необходимости изменить пароли
```

### 2. Запуск системы

#### Автоматический запуск (рекомендуется):
```bash
# Запустить скрипт автоматического развертывания
./start.sh
```

#### Ручной запуск:
```bash
# 1. Создать Docker сеть
docker network create app-shared-network

# 2. Запустить инфраструктуру
docker-compose -f docker-compose.main.yml up -d rabbit postgres elasticsearch redis

# 3. Подождать готовности (30 сек)
sleep 30

# 4. Запустить сервисы приложения
docker-compose -f docker-compose.main.yml up -d catalog-service-api order-service-api notification-service

# 5. Подождать готовности (20 сек)  
sleep 20

# 6. Запустить API Gateway
docker-compose -f docker-compose.main.yml up -d api-gateway
```

### 3. Проверка работы
```bash
# Health check
curl http://localhost:8000/health

# Получить товары
curl http://localhost:8000/api/products

# Создать заказ
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": "123e4567-e89b-12d3-a456-426614174000"}'
```

### 4. Диагностика проблем
```bash
# Запустить скрипт диагностики
./debug.sh

# Посмотреть логи
docker-compose -f docker-compose.main.yml logs -f

# Перезапустить систему
docker-compose -f docker-compose.main.yml down
./start.sh
```

## 📚 API документация

### Единый API через Gateway
**Base URL**: `http://localhost:8000`

#### Публичные эндпоинты:
- `GET /api/products` - Получить товары с фильтрами
- `GET /api/products/{id}` - Получить товар по ID
- `POST /api/orders` - Создать заказ
- `GET /api/orders/{id}` - Получить статус заказа

#### Админские эндпоинты (Authorization: Bearer admin_master_key_2024):
- `POST /api/products` - Создать товар
- `PATCH /api/products/{id}` - Обновить товар
- `DELETE /api/products/{id}` - Удалить товар
- `GET /api/orders` - Получить все заказы
- `PATCH /api/orders/{id}` - Обновить статус заказа

**Подробная документация**: [API Gateway Docs](api_gateway/API_GATEWAY_DOCS.md)

## 🔧 Сервисы

### 1. API Gateway (Nginx)
- **Порт**: 8000
- **Функция**: Единая точка входа, роутинг запросов
- **Конфигурация**: [nginx.conf](api_gateway/nginx.conf)

### 2. Catalog Service (FastAPI)
- **Порт**: 8001 (внутренний)
- **База данных**: Elasticsearch + Redis
- **Функции**: Управление товарами, поиск, фильтрация

### 3. Order Service (FastAPI)  
- **Порт**: 8080 (внутренний)
- **База данных**: PostgreSQL
- **Функции**: Создание заказов, управление статусами

### 4. Notification Service (FastStream)
- **Функции**: Telegram уведомления через RabbitMQ
- **Интеграция**: Telegram Bot API

## 📁 Структура проекта

```
backend/
├── api_gateway/           # Nginx Gateway
│   ├── nginx.conf
│   ├── docker-compose.yml
│   └── API_GATEWAY_DOCS.md
├── catalog_service/       # Каталог товаров
│   ├── src/
│   ├── requirements.txt
│   └── API_EXAMPLES.md
├── order_service/         # Управление заказами
│   ├── src/
│   ├── requirements.txt
│   └── ORDER_API_DOCS.md
├── notification-service/  # Telegram уведомления
│   ├── src/
│   └── requirements.txt
├── rabbitmq/             # RabbitMQ конфигурация
├── docker-compose.main.yml # Главный docker-compose
└── CLAUDE.md             # Документация для AI
```

## 🔐 Безопасность

### Единый админский ключ
Все админские операции используют единый API ключ: `admin_master_key_2024`

### Конфигурация
В каждом сервисе в файле `.env`:
```env
admin_api_key=admin_master_key_2024
```

## 🔄 Telegram уведомления

### Настройка бота:
1. Создать бота через @BotFather
2. Получить токен бота
3. Добавить бота в чат
4. Получить chat_id через API
5. Установить переменные в `.env`

### События:
- Создание заказа: "Новый заказ создан! ID: 1, Товар: {product_id}"
- Оплата: "Заказ #1 оплачен!"
- Отправка: "Заказ #1 отправлен!"
- Доставка: "Заказ #1 доставлен!"

## 🛠️ Разработка

### Запуск отдельных сервисов:
```bash
# Catalog Service
cd catalog_service && make run

# Order Service  
cd order_service && make run

# Notification Service
cd notification-service && make run
```

### Логи и мониторинг:
```bash
# Все логи
docker-compose -f docker-compose.main.yml logs -f

# Конкретный сервис
docker logs api-gateway -f
docker logs catalog-service-api -f
docker logs order-service-api -f
```

## 🔧 Зависимости

### Системные требования:
- Docker & Docker Compose
- 4GB+ RAM
- 10GB+ свободного места

### Внешние сервисы:
- PostgreSQL 16
- Elasticsearch 7.17
- Redis Alpine
- RabbitMQ Management
- Nginx Alpine

## 📝 Примеры использования

### Фронтенд интеграция:
```javascript
// Получение товаров
const products = await fetch('http://localhost:8000/api/products');

// Создание заказа
const order = await fetch('http://localhost:8000/api/orders', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({product_id: 'uuid-here'})
});

// Админские операции
const adminHeaders = {
  'Authorization': 'Bearer admin_master_key_2024'
};
```

## 🚨 Troubleshooting

### Основные проблемы и решения:

#### 1. **Сервисы завершаются сразу (exit code 0)**
```bash
# Решение: Используйте автоматический запуск
./start.sh

# Или проверьте логи
docker-compose -f docker-compose.main.yml logs catalog-service-api
```

#### 2. **Gateway не находит сервисы (host not found in upstream)**
```bash
# Убедитесь что сервисы запущены
docker-compose -f docker-compose.main.yml ps

# Перезапустите в правильном порядке
docker-compose -f docker-compose.main.yml down
./start.sh
```

#### 3. **Сеть не создана**
```bash
docker network create app-shared-network
```

#### 4. **Порты заняты**
```bash
# Найти процессы на нужных портах
sudo lsof -i :8000
sudo lsof -i :5432

# Остановить конфликтующие контейнеры
docker stop $(docker ps -q)
```

#### 5. **Telegram не работает**
```bash
# Проверить переменные в notification-service/.env
cat notification-service/.env | grep TELEGRAM

# Проверить логи
docker logs notification-service -f
```

### Скрипты для диагностики:
```bash
# Автоматическая диагностика
./debug.sh

# Статус всех контейнеров
docker-compose -f docker-compose.main.yml ps

# Логи конкретного сервиса
docker-compose -f docker-compose.main.yml logs -f service-name

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.main.yml restart service-name
```

### Полный сброс системы:
```bash
# Остановить и удалить всё
docker-compose -f docker-compose.main.yml down -v
docker system prune -f

# Заново запустить
./start.sh
```