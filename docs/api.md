# API Reference

## Health

### `GET /health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Users

### `POST /v1/users/`

Create a new user.

**Request**:
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### `GET /v1/users/{user_id}`

Retrieve a user by ID.

### `PATCH /v1/users/{user_id}`

Update a user's name or email.

**Request**:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

## Orders

### `POST /v1/orders/`

Place a new order.

**Request**:
```json
{
  "items": [{"product_id": "uuid", "quantity": 2}],
  "shipping_street": "123 Main St",
  "shipping_city": "Springfield",
  "shipping_state": "IL",
  "shipping_zip": "62701",
  "shipping_country": "US"
}
```

### `GET /v1/orders/?user_id={user_id}`

List orders for a user.

## Products

### `POST /v1/products/`

Create a new product.

**Request**:
```json
{
  "name": "Widget",
  "description": "A useful widget",
  "price": 9.99,
  "stock_quantity": 100
}
```

### `GET /v1/products/{product_id}`

Retrieve a product by ID.

### `GET /v1/products/`

List all products.
