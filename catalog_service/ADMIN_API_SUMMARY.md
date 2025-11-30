# Admin API Summary

## Реализованные админские эндпоинты

### 🔐 Авторизация
- Простая авторизация через API ключ в заголовке `Authorization: Bearer {admin_api_key}`
- API ключ админа настраивается в `.env` файле: `admin_api_key=super_secret_admin_key_2024`
- При неправильном ключе возвращается 401 Unauthorized

### 📝 Эндпоинты

#### 1. **POST /api/products** - Создание товара
- Требует админские права
- Принимает полную информацию о товаре
- Возвращает созданный продукт с ID
- Ответ: 201 Created + ProductResponse

#### 2. **PATCH /api/products/{id}** - Обновление товара
- Требует админские права  
- Частичное обновление (title, description, amount, price)
- Ответ: 200 OK + {"success": true}
- 404 если товар не найден

#### 3. **DELETE /api/products/{id}** - Удаление товара
- Требует админские права
- Полное удаление товара из Elasticsearch и кэша Redis
- Ответ: 200 OK + {"success": true}
- 404 если товар не найден

### 🔧 Технические детали

#### Конфигурация
- Новый параметр `admin_api_key` в `Settings`
- Пример в `.env.example`

#### Авторизация
- Функция `verify_admin_token()` в `src/api/dependencies/auth.py`
- Проверяет формат: `Bearer {admin_api_key}`

#### Безопасность
- API ключ передается в заголовке, а не в URL
- Все админские операции требуют валидный токен
- Четкое разделение прав доступа

### 📄 Примеры использования

#### Создание продукта
```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Authorization: Bearer super_secret_admin_key_2024" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "iPhone 15 Pro",
    "category_id": 1,
    "description": "Latest iPhone",
    "characteristics": {
      "type": "телефон",
      "brand": "Apple",
      "color": "черный",
      "memory": "128GB"
    },
    "created_at": "2024-01-01T10:00:00",
    "amount": 10,
    "price": 99999.0
  }'
```

#### Обновление продукта
```bash
curl -X PATCH "http://localhost:8000/api/products/550e8400-e29b-41d4-a716-446655440001" \
  -H "Authorization: Bearer super_secret_admin_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"price": 89999.0, "amount": 5}'
```

#### Удаление продукта
```bash
curl -X DELETE "http://localhost:8000/api/products/550e8400-e29b-41d4-a716-446655440001" \
  -H "Authorization: Bearer super_secret_admin_key_2024"
```

### ✅ Статус реализации
- [x] Простая авторизация через API ключ
- [x] POST /products с админскими правами
- [x] PATCH /products/{id} с админскими правами  
- [x] DELETE /products/{id} с админскими правами
- [x] Обработка ошибок авторизации (401)
- [x] Обработка ошибок "не найден" (404)
- [x] Response models для консистентности API
- [x] Документация с примерами использования