# Catalog Service API Examples

## GET /api/products

### Basic Usage
```bash
GET /api/products
```

### Electronics Store Filters

#### Filter by Product Type
```bash
GET /api/products?product_type=телефон
GET /api/products?product_type=планшет
GET /api/products?product_type=ноутбук
GET /api/products?product_type=наушники
```

#### Filter by Brand
```bash
GET /api/products?brand=Apple
GET /api/products?brand=Samsung
GET /api/products?brand=Xiaomi
```

#### Filter by Color
```bash
GET /api/products?color=черный
GET /api/products?color=белый
GET /api/products?color=синий
```

#### Filter by Memory/Storage
```bash
GET /api/products?memory=128GB
GET /api/products?memory=256GB
GET /api/products?memory=8GB
```

#### Price Range Filters
```bash
GET /api/products?price_min=10000
GET /api/products?price_max=50000
GET /api/products?price_min=20000&price_max=80000
```

#### Pagination
```bash
GET /api/products?limit=20&offset=0
GET /api/products?limit=20&offset=20
```

#### Combined Filters
```bash
GET /api/products?product_type=телефон&brand=Apple&memory=128GB&price_min=50000&price_max=120000
```

### Response Format
```json
{
    "products": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "iPhone 15 Pro",
            "category_id": 1,
            "description": "Latest iPhone with advanced features",
            "characteristics": {
                "type": "телефон",
                "brand": "Apple",
                "color": "черный",
                "memory": "128GB",
                "display": "6.1 inch",
                "camera": "48MP"
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

## GET /api/products/{id}

### Get Product by ID
```bash
GET /api/products/123e4567-e89b-12d3-a456-426614174000
```

### Response Format
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "iPhone 15 Pro",
    "category_id": 1,
    "description": "Latest iPhone with advanced features",
    "characteristics": {
        "type": "телефон",
        "brand": "Apple",
        "color": "черный",
        "memory": "128GB",
        "display": "6.1 inch",
        "camera": "48MP"
    },
    "created_at": "2024-01-01T00:00:00",
    "amount": 10,
    "price": 99999.0
}
```

### Error Response (404)
```json
{
    "detail": "Product with id = 123e4567-e89b-12d3-a456-426614174000 does not exist"
}
```

## Product Characteristics Schema for Electronics

For electronics products, the `characteristics` field should contain:

### Common Fields
- `type`: Product type (телефон, планшет, ноутбук, наушники, etc.)
- `brand`: Manufacturer brand
- `color`: Product color
- `memory`: Storage/RAM capacity

### Type-specific Fields

#### For Phones (телефон):
- `display`: Screen size
- `camera`: Camera specifications
- `battery`: Battery capacity
- `os`: Operating system

#### For Laptops (ноутбук):
- `cpu`: Processor model
- `ram`: RAM amount
- `storage`: Storage type and capacity
- `display`: Screen size and resolution
- `gpu`: Graphics card

#### For Tablets (планшет):
- `display`: Screen size
- `battery`: Battery capacity
- `os`: Operating system
- `cellular`: Cellular support

#### For Headphones (наушники):
- `type`: Over-ear, in-ear, etc.
- `wireless`: Wireless connectivity
- `noise_cancelling`: Active noise cancellation
- `battery`: Battery life (for wireless)

## Admin Endpoints (Authorization Required)

All admin endpoints require the `Authorization` header with admin API key:
```
Authorization: Bearer super_secret_admin_key_2024
```

### POST /api/products - Create Product

```bash
POST /api/products
Authorization: Bearer super_secret_admin_key_2024
Content-Type: application/json

{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "iPhone 15 Pro Max",
    "category_id": 1,
    "description": "Flagship iPhone with the most advanced features",
    "characteristics": {
        "type": "телефон",
        "brand": "Apple",
        "color": "титановый",
        "memory": "256GB",
        "display": "6.7 inch",
        "camera": "48MP Pro",
        "battery": "4422 mAh",
        "os": "iOS 17"
    },
    "created_at": "2024-01-01T10:00:00",
    "amount": 50,
    "price": 129999.0
}
```

**Response (201):**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "iPhone 15 Pro Max",
    "category_id": 1,
    "description": "Flagship iPhone with the most advanced features",
    "characteristics": {
        "type": "телефон",
        "brand": "Apple",
        "color": "титановый",
        "memory": "256GB",
        "display": "6.7 inch",
        "camera": "48MP Pro",
        "battery": "4422 mAh",
        "os": "iOS 17"
    },
    "created_at": "2024-01-01T10:00:00",
    "amount": 50,
    "price": 129999.0
}
```

### PATCH /api/products/{id} - Update Product

```bash
PATCH /api/products/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer super_secret_admin_key_2024
Content-Type: application/json

{
    "price": 119999.0,
    "amount": 75,
    "description": "iPhone 15 Pro Max - now with special discount!"
}
```

**Response (200):**
```json
{
    "success": true
}
```

### DELETE /api/products/{id} - Delete Product

```bash
DELETE /api/products/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer super_secret_admin_key_2024
```

**Response (200):**
```json
{
    "success": true
}
```

### Authorization Errors

**Missing or invalid API key (401):**
```json
{
    "detail": "Invalid or missing admin API token"
}
```

**Product not found (404):**
```json
{
    "detail": "Product with id = 123e4567-e89b-12d3-a456-426614174000 does not exist"
}
```

## Example Electronics Products

### Smartphone Example
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Samsung Galaxy S24 Ultra",
    "category_id": 1,
    "description": "Premium Android smartphone with S Pen",
    "characteristics": {
        "type": "телефон",
        "brand": "Samsung",
        "color": "черный",
        "memory": "512GB",
        "ram": "12GB",
        "display": "6.8 inch Dynamic AMOLED",
        "camera": "200MP + 50MP + 12MP + 10MP",
        "battery": "5000 mAh",
        "os": "Android 14"
    },
    "created_at": "2024-01-15T12:00:00",
    "amount": 30,
    "price": 139999.0
}
```

### Laptop Example
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "title": "MacBook Air M3 15\"",
    "category_id": 2,
    "description": "Lightweight laptop with Apple M3 chip",
    "characteristics": {
        "type": "ноутбук",
        "brand": "Apple",
        "color": "серебристый",
        "memory": "512GB SSD",
        "ram": "16GB",
        "cpu": "Apple M3",
        "gpu": "10-core GPU",
        "display": "15.3 inch Liquid Retina",
        "battery": "до 18 часов",
        "os": "macOS Sonoma"
    },
    "created_at": "2024-01-20T14:30:00",
    "amount": 15,
    "price": 189999.0
}
```