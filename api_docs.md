# API Documentation - E-commerce Backend

## Base URL
```
http://localhost:8000
```

## Authentication
Admin endpoints require Bearer token:
```
Authorization: Bearer admin_master_key_2024
```

---

## Products API (`/api/products`)

### GET /api/products
Get products with filters

**Query Parameters:**
- `title` (string, optional) - Product name filter
- `product_type` (string, optional) - Product type: телефон, планшет, ноутбук, наушники
- `color` (string, optional) - Product color
- `memory` (string, optional) - Memory/storage size
- `price_min` (number, optional) - Minimum price
- `price_max` (number, optional) - Maximum price
- `brand` (string, optional) - Product brand
- `limit` (integer, optional, default: 50, max: 100) - Limit results
- `offset` (integer, optional, default: 0) - Offset for pagination

**Response:**
```json
{
  "products": [
    {
      "id": "uuid",
      "title": "string",
      "category_id": 1,
      "description": "string",
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
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### GET /api/products/{id}
Get product by ID

**Path Parameters:**
- `id` (uuid) - Product ID

**Response:**
```json
{
  "id": "uuid",
  "title": "string",
  "category_id": 1,
  "description": "string",
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

### POST /api/products 🔐
Create product (admin only)

**Headers:**
- `Authorization: Bearer admin_master_key_2024`

**Request Body:**
```json
{
  "id": "uuid",
  "title": "string",
  "category_id": 1,
  "description": "string",
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

### PATCH /api/products/{id} 🔐
Update product (admin only)

**Headers:**
- `Authorization: Bearer admin_master_key_2024`

**Path Parameters:**
- `id` (uuid) - Product ID

**Request Body:** (partial update)
```json
{
  "price": 89999.0,
  "amount": 15
}
```

### DELETE /api/products/{id} 🔐
Delete product (admin only)

**Headers:**
- `Authorization: Bearer admin_master_key_2024`

**Path Parameters:**
- `id` (uuid) - Product ID

---

## Orders API (`/api/orders`)

### POST /api/orders
Create order

**Request Body:**
```json
"product-uuid-string"
```

**Response:**
```json
{
  "id": 1,
  "product_id": "uuid",
  "status": "created",
  "amount": 1,
  "price": 99999.0,
  "created_at": "2024-01-01T00:00:00",
  "paid_at": null,
  "shipped_at": null,
  "delivered_at": null
}
```

### GET /api/orders/{id}
Get order by ID

**Path Parameters:**
- `id` (integer) - Order ID

**Response:**
```json
{
  "id": 1,
  "product_id": "uuid",
  "status": "created",
  "amount": 1,
  "price": 99999.0,
  "created_at": "2024-01-01T00:00:00",
  "paid_at": null,
  "shipped_at": null,
  "delivered_at": null
}
```

### POST /api/orders/{id}/confirm
Confirm order

**Path Parameters:**
- `id` (integer) - Order ID

### GET /api/orders 🔐
Get all orders (admin only)

**Headers:**
- `Authorization: Bearer admin_master_key_2024`

**Query Parameters:**
- `limit` (integer, optional, default: 100, max: 1000) - Limit results
- `offset` (integer, optional, default: 0) - Offset for pagination

**Response:**
```json
{
  "orders": [
    {
      "id": 1,
      "product_id": "uuid",
      "status": "created",
      "amount": 1,
      "price": 99999.0,
      "created_at": "2024-01-01T00:00:00",
      "paid_at": null,
      "shipped_at": null,
      "delivered_at": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0
}
```

### PATCH /api/orders/{id} 🔐
Update order status (admin only)

**Headers:**
- `Authorization: Bearer admin_master_key_2024`

**Path Parameters:**
- `id` (integer) - Order ID

**Request Body:**
```json
{
  "status": "delivered"
}
```

**Available statuses:**
- `created`
- `paid`
- `shipped`
- `in_transit`
- `delivered`
- `cancelled`

---

## System Endpoints

### GET /health
Health check

**Response:**
```
Gateway is healthy
```

### GET /docs
Main documentation (redirects to catalog docs)

### GET /catalog-docs
Catalog service Swagger UI

### GET /orders-docs
Order service Swagger UI

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing admin API token"
}
```

### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "title"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

---

## Frontend Integration Notes

### CORS
All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Authorization, Content-Type`

### Content-Type
Always use `Content-Type: application/json` for POST/PATCH requests.

### Product Characteristics
Electronics products have standardized characteristics:
- `type`: телефон | планшет | ноутбук | наушники
- `brand`: Apple | Samsung | Xiaomi | etc.
- `color`: черный | белый | синий | etc.
- `memory`: 64GB | 128GB | 256GB | etc.

### Order Status Flow
```
created → paid → shipped → in_transit → delivered
                     ↓
                 cancelled (can be set at any time)
```

### Pagination
All list endpoints support:
- `limit` - number of items per page
- `offset` - number of items to skip
- Response includes `total`, `limit`, `offset`

