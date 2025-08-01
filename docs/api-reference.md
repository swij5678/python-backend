# API Reference

This document provides detailed information about the Python Service REST API endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, you would typically use:

- API Keys
- JWT Tokens
- OAuth 2.0

## Health Endpoints

### Health Check

Check if the service is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-31T10:00:00Z",
  "version": "1.0.0",
  "uptime": 3600
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

### Readiness Check

Check if the service is ready to accept requests.

**Endpoint:** `GET /ready`

**Response:**
```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "external_api": "ok"
  }
}
```

## Items API

### Get All Items

Retrieve a list of all items.

**Endpoint:** `GET /api/v1/items`

**Query Parameters:**
- `limit` (optional): Maximum number of items to return (default: 100)
- `offset` (optional): Number of items to skip (default: 0)
- `search` (optional): Search term to filter items

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/items?limit=10&offset=0&search=test"
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Test Item",
      "description": "A test item",
      "created_at": "2025-07-31T10:00:00Z",
      "updated_at": "2025-07-31T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Items retrieved successfully
- `400 Bad Request`: Invalid query parameters

### Get Item by ID

Retrieve a specific item by its ID.

**Endpoint:** `GET /api/v1/items/{item_id}`

**Path Parameters:**
- `item_id` (required): The unique identifier of the item

**Example Request:**
```bash
curl http://localhost:8000/api/v1/items/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Test Item",
  "description": "A test item",
  "created_at": "2025-07-31T10:00:00Z",
  "updated_at": "2025-07-31T10:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Item found and returned
- `404 Not Found`: Item not found

### Create Item

Create a new item.

**Endpoint:** `POST /api/v1/items`

**Request Body:**
```json
{
  "name": "New Item",
  "description": "Description of the new item"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Item",
    "description": "Description of the new item"
  }'
```

**Response:**
```json
{
  "id": 2,
  "name": "New Item",
  "description": "Description of the new item",
  "created_at": "2025-07-31T10:30:00Z",
  "updated_at": "2025-07-31T10:30:00Z"
}
```

**Status Codes:**
- `201 Created`: Item created successfully
- `400 Bad Request`: Invalid request data
- `422 Unprocessable Entity`: Validation errors

### Update Item

Update an existing item.

**Endpoint:** `PUT /api/v1/items/{item_id}`

**Path Parameters:**
- `item_id` (required): The unique identifier of the item

**Request Body:**
```json
{
  "name": "Updated Item",
  "description": "Updated description"
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Item",
    "description": "Updated description"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Item",
  "description": "Updated description",
  "created_at": "2025-07-31T10:00:00Z",
  "updated_at": "2025-07-31T10:45:00Z"
}
```

**Status Codes:**
- `200 OK`: Item updated successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Item not found
- `422 Unprocessable Entity`: Validation errors

### Delete Item

Delete an item by its ID.

**Endpoint:** `DELETE /api/v1/items/{item_id}`

**Path Parameters:**
- `item_id` (required): The unique identifier of the item

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/v1/items/1
```

**Response:**
```json
{
  "message": "Item deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Item deleted successfully
- `404 Not Found`: Item not found

## Data Models

### Item Model

```json
{
  "id": "integer (read-only)",
  "name": "string (required, max 100 characters)",
  "description": "string (optional, max 500 characters)",
  "created_at": "datetime (read-only)",
  "updated_at": "datetime (read-only)"
}
```

### Error Model

```json
{
  "error": "string",
  "message": "string",
  "details": "object (optional)"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Rate Limit**: 100 requests per minute per IP
- **Headers**: 
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

When rate limit is exceeded:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please try again later."
}
```

## Error Handling

The API uses standard HTTP status codes and returns consistent error responses:

### Common Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional error details"
  }
}
```

## Interactive Documentation

You can explore the API interactively using:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These tools allow you to:
- View all endpoints
- Test API calls
- See request/response schemas
- Download OpenAPI specification
