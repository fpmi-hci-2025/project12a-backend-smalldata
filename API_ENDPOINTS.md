# 🌐 API Endpoints - E-commerce Backend

## Base URL: `http://localhost:8000`

---

## 📋 **Swagger Documentation**

### **Catalog Service (Products)**
- 🔗 **Swagger UI**: http://localhost:8000/catalog-docs
- 📄 **OpenAPI Spec**: http://localhost:8000/catalog-openapi.json

### **Order Service (Orders)**
- 🔗 **Swagger UI**: http://localhost:8000/orders-docs
- 📄 **OpenAPI Spec**: http://localhost:8000/orders-openapi.json

### **Default Docs**
- 🔗 **Main Docs** (redirects to catalog): http://localhost:8000/docs

---

## 🛒 **Products API** (`/api/products`)

### **Public Endpoints:**

#### **GET /api/products** - Get Products with Filters
```bash
curl "http://localhost:8000/api/products?product_type=телефон&brand=Apple&price_max=100000&limit=20"
```

**Response:**
```json
{
    "products": [],
    "total": 0,
    "limit": 50,
    "offset": 0
}
```

#### **GET /api/products/{id}** - Get Product by ID
```bash
curl "http://localhost:8000/api/products/123e4567-e89b-12d3-a456-426614174000"
```

### **Admin Endpoints** (Authorization: Bearer admin_master_key_2024):

#### **POST /api/products** - Create Product
```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Authorization: Bearer admin_master_key_2024" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "iPhone 15 Pro",
    "category_id": 1,
    "description": "Latest iPhone",
    "characteristics": {
      "type": "телефон",
      "brand": "Apple",
      "color": "черный",
      "memory": "128GB"
    },
    "created_at": "2024-01-01T00:00:00",
    "amount": 10,
    "price": 99999.0
  }'
```

#### **PATCH /api/products/{id}** - Update Product
```bash
curl -X PATCH "http://localhost:8000/api/products/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer admin_master_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"price": 89999.0, "amount": 15}'
```

#### **DELETE /api/products/{id}** - Delete Product
```bash
curl -X DELETE "http://localhost:8000/api/products/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer admin_master_key_2024"
```

---

## 📦 **Orders API** (`/api/orders`)

### **Public Endpoints:**

#### **POST /api/orders** - Create Order
```bash
curl -X POST "http://localhost:8000/api/orders" \
  -H "Content-Type: application/json" \
  -d '"123e4567-e89b-12d3-a456-426614174000"'
```

#### **GET /api/orders/{id}** - Get Order Status
```bash
curl "http://localhost:8000/api/orders/1"
```

#### **POST /api/orders/{id}/confirm** - Confirm Order
```bash
curl -X POST "http://localhost:8000/api/orders/1/confirm"
```

### **Admin Endpoints** (Authorization: Bearer admin_master_key_2024):

#### **GET /api/orders** - Get All Orders
```bash
curl "http://localhost:8000/api/orders?limit=50&offset=0" \
  -H "Authorization: Bearer admin_master_key_2024"
```

#### **PATCH /api/orders/{id}** - Update Order Status
```bash
curl -X PATCH "http://localhost:8000/api/orders/1" \
  -H "Authorization: Bearer admin_master_key_2024" \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered"}'
```

**Available statuses:** `created`, `paid`, `shipped`, `in_transit`, `delivered`, `cancelled`

---

## 🔐 **Authentication**

### **Admin API Key**
```
Authorization: Bearer admin_master_key_2024
```

### **Endpoints requiring admin auth:**
- `POST /api/products`
- `PATCH /api/products/{id}`
- `DELETE /api/products/{id}`
- `GET /api/orders`
- `PATCH /api/orders/{id}`

---

## 🏥 **System Endpoints**

### **Health Check**
```bash
curl http://localhost:8000/health
```
**Response:** `Gateway is healthy`

---

## 📱 **Frontend Integration Examples**

### **JavaScript/TypeScript**
```javascript
const API_BASE = 'http://localhost:8000';

// Get products
const products = await fetch(`${API_BASE}/api/products?product_type=телефон`);
const data = await products.json();

// Create order
const order = await fetch(`${API_BASE}/api/orders`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: '"product-uuid-here"'
});

// Admin operations
const adminHeaders = {
  'Authorization': 'Bearer admin_master_key_2024',
  'Content-Type': 'application/json'
};

const newProduct = await fetch(`${API_BASE}/api/products`, {
  method: 'POST',
  headers: adminHeaders,
  body: JSON.stringify(productData)
});
```

### **React Hook Example**
```javascript
import { useState, useEffect } from 'react';

function useProducts(filters = {}) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const params = new URLSearchParams(filters);
    fetch(`http://localhost:8000/api/products?${params}`)
      .then(res => res.json())
      .then(data => {
        setProducts(data.products);
        setLoading(false);
      });
  }, [filters]);
  
  return { products, loading };
}
```

---

## 🚀 **Quick Start Testing**

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Get empty products list
curl http://localhost:8000/api/products

# 3. Create a test product (admin)
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer admin_master_key_2024" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Test iPhone",
    "category_id": 1,
    "description": "Test product",
    "characteristics": {"type": "телефон", "brand": "Apple"},
    "created_at": "2024-01-01T00:00:00",
    "amount": 5,
    "price": 50000
  }'

# 4. Get products (should now show 1)
curl http://localhost:8000/api/products

# 5. Create order for the product
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '"550e8400-e29b-41d4-a716-446655440001"'

# 6. Check order status
curl http://localhost:8000/api/orders/1
```

---

## 🐛 **Troubleshooting**

### **Common Issues:**
1. **404 errors**: Make sure all services are running: `docker-compose -f docker-compose.main.yml ps`
2. **503 errors**: Services might be starting up, wait 30 seconds
3. **CORS errors**: API Gateway handles CORS automatically
4. **Auth errors**: Check if admin key is correct: `admin_master_key_2024`

### **Logs:**
```bash
# Gateway logs
docker logs api-gateway -f

# Service logs
docker-compose -f docker-compose.main.yml logs -f
```