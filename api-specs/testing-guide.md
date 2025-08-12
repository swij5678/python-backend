# API Testing Guide

This document provides comprehensive testing strategies and examples for the Python Service API.

## Table of Contents
- [Testing Strategy](#testing-strategy)
- [Manual Testing](#manual-testing)
- [Automated Testing](#automated-testing)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)
- [Test Data](#test-data)

## Testing Strategy

### Testing Pyramid
1. **Unit Tests**: Individual endpoint logic
2. **Integration Tests**: API contract testing
3. **End-to-End Tests**: Complete user workflows
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: Vulnerability assessment

### Test Environments
- **Local Development**: `http://localhost:8000`
- **Testing**: `https://test-api.example.com`
- **Staging**: `https://staging-api.example.com`
- **Production**: `https://api.example.com`

## Manual Testing

### Using Postman
1. Import the `postman-collection.json` file
2. Set environment variables:
   - `baseUrl`: Your API base URL
   - `itemId`: Test item ID
3. Run the collection or individual requests

### Using cURL

#### Health Checks
```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Readiness check
curl -X GET "http://localhost:8000/ready"
```

#### Items CRUD Operations
```bash
# Create an item
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Item",
    "description": "A test item for API testing"
  }'

# Get all items
curl -X GET "http://localhost:8000/api/v1/items"

# Get items with pagination
curl -X GET "http://localhost:8000/api/v1/items?limit=5&offset=0"

# Search items
curl -X GET "http://localhost:8000/api/v1/items?search=test"

# Get specific item (replace 1 with actual item ID)
curl -X GET "http://localhost:8000/api/v1/items/1"

# Update an item
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Test Item",
    "description": "Updated description"
  }'

# Delete an item
curl -X DELETE "http://localhost:8000/api/v1/items/1"
```

### Using HTTPie
```bash
# Install HTTPie: pip install httpie

# Create an item
http POST localhost:8000/api/v1/items name="Test Item" description="Test description"

# Get all items
http GET localhost:8000/api/v1/items

# Get items with search
http GET localhost:8000/api/v1/items search==test

# Update an item
http PUT localhost:8000/api/v1/items/1 name="Updated Item" description="Updated"

# Delete an item
http DELETE localhost:8000/api/v1/items/1
```

## Automated Testing

### Test Cases

#### Health Endpoints
- ✅ Health check returns 200 with correct schema
- ✅ Readiness check returns 200 with correct schema
- ✅ Health check includes version and uptime
- ✅ Readiness check includes dependency status

#### Items API - GET /api/v1/items
- ✅ Returns empty array when no items exist
- ✅ Returns all items when items exist
- ✅ Respects limit parameter
- ✅ Respects offset parameter
- ✅ Filters by search term in name
- ✅ Filters by search term in description
- ✅ Returns 400 for invalid limit values
- ✅ Returns 400 for invalid offset values

#### Items API - POST /api/v1/items
- ✅ Creates item with valid data
- ✅ Returns 201 with created item
- ✅ Auto-generates ID and timestamps
- ✅ Returns 422 for missing name
- ✅ Returns 422 for invalid data types
- ✅ Handles optional description field
- ✅ Validates name length constraints
- ✅ Validates description length constraints

#### Items API - GET /api/v1/items/{id}
- ✅ Returns item for valid ID
- ✅ Returns 404 for non-existent ID
- ✅ Returns 422 for invalid ID format

#### Items API - PUT /api/v1/items/{id}
- ✅ Updates existing item with valid data
- ✅ Returns updated item with new timestamp
- ✅ Returns 404 for non-existent ID
- ✅ Returns 422 for invalid data
- ✅ Preserves created_at timestamp
- ✅ Updates updated_at timestamp

#### Items API - DELETE /api/v1/items/{id}
- ✅ Deletes existing item
- ✅ Returns success message
- ✅ Returns 404 for non-existent ID
- ✅ Returns 422 for invalid ID format

### Python Test Examples

```python
import pytest
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

class TestHealthEndpoints:
    def test_health_check(self):
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"

    def test_readiness_check(self):
        response = requests.get(f"{BASE_URL}/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert data["status"] == "ready"

class TestItemsAPI:
    def test_create_item(self):
        payload = {
            "name": "Test Item",
            "description": "Test description"
        }
        response = requests.post(f"{BASE_URL}/api/v1/items", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["description"] == payload["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_items(self):
        response = requests.get(f"{BASE_URL}/api/v1/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_item_missing_name(self):
        payload = {"description": "Missing name"}
        response = requests.post(f"{BASE_URL}/api/v1/items", json=payload)
        assert response.status_code == 422

    def test_get_nonexistent_item(self):
        response = requests.get(f"{BASE_URL}/api/v1/items/99999")
        assert response.status_code == 404
```

### JavaScript Test Examples

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

describe('Python Service API', () => {
  describe('Health Endpoints', () => {
    test('health check should return 200', async () => {
      const response = await axios.get(`${BASE_URL}/health`);
      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('status', 'healthy');
      expect(response.data).toHaveProperty('version');
      expect(response.data).toHaveProperty('timestamp');
    });

    test('readiness check should return 200', async () => {
      const response = await axios.get(`${BASE_URL}/ready`);
      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('status', 'ready');
      expect(response.data).toHaveProperty('checks');
    });
  });

  describe('Items API', () => {
    let createdItemId;

    test('should create a new item', async () => {
      const payload = {
        name: 'Test Item',
        description: 'Test description'
      };
      const response = await axios.post(`${BASE_URL}/api/v1/items`, payload);
      expect(response.status).toBe(201);
      expect(response.data.name).toBe(payload.name);
      expect(response.data).toHaveProperty('id');
      createdItemId = response.data.id;
    });

    test('should get all items', async () => {
      const response = await axios.get(`${BASE_URL}/api/v1/items`);
      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });

    test('should get item by ID', async () => {
      const response = await axios.get(`${BASE_URL}/api/v1/items/${createdItemId}`);
      expect(response.status).toBe(200);
      expect(response.data.id).toBe(createdItemId);
    });

    test('should update item', async () => {
      const payload = {
        name: 'Updated Item',
        description: 'Updated description'
      };
      const response = await axios.put(`${BASE_URL}/api/v1/items/${createdItemId}`, payload);
      expect(response.status).toBe(200);
      expect(response.data.name).toBe(payload.name);
    });

    test('should delete item', async () => {
      const response = await axios.delete(`${BASE_URL}/api/v1/items/${createdItemId}`);
      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('message');
    });

    test('should return 404 for non-existent item', async () => {
      try {
        await axios.get(`${BASE_URL}/api/v1/items/99999`);
      } catch (error) {
        expect(error.response.status).toBe(404);
      }
    });
  });
});
```

## Performance Testing

### Load Testing with Artillery
```yaml
# artillery-config.yml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 5
    - duration: 120
      arrivalRate: 10
    - duration: 60
      arrivalRate: 20

scenarios:
  - name: "Health Check"
    weight: 30
    flow:
      - get:
          url: "/health"
  
  - name: "Get Items"
    weight: 50
    flow:
      - get:
          url: "/api/v1/items"
  
  - name: "Create and Delete Item"
    weight: 20
    flow:
      - post:
          url: "/api/v1/items"
          json:
            name: "Load Test Item {{ $randomString() }}"
            description: "Generated during load test"
      - delete:
          url: "/api/v1/items/{{ id }}"
```

Run with: `artillery run artillery-config.yml`

### Load Testing with Apache Bench
```bash
# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test get items endpoint
ab -n 1000 -c 10 http://localhost:8000/api/v1/items
```

## Security Testing

### Input Validation Tests
- SQL injection attempts
- XSS payload injection
- Command injection
- Buffer overflow attempts
- Invalid JSON payloads
- Malformed requests

### Security Headers Tests
```bash
# Check security headers
curl -I http://localhost:8000/health

# Expected security headers:
# - X-Content-Type-Options: nosniff
# - X-Frame-Options: DENY
# - X-XSS-Protection: 1; mode=block
```

## Test Data

### Sample Items
```json
[
  {
    "name": "Sample Item 1",
    "description": "This is the first sample item"
  },
  {
    "name": "Sample Item 2",
    "description": "This is the second sample item"
  },
  {
    "name": "Test Product",
    "description": "A product for testing search functionality"
  },
  {
    "name": "Demo Widget",
    "description": null
  }
]
```

### Edge Cases
- Empty strings
- Very long strings
- Unicode characters
- Special characters
- HTML tags
- JSON injection attempts

## Continuous Integration

### GitHub Actions Example
```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Start API server
        run: |
          python src/main.py &
          sleep 10
      - name: Run tests
        run: pytest tests/
      - name: Run integration tests
        run: python tests/integration_tests.py
```

## Monitoring and Alerting

### Key Metrics to Monitor
- Response time percentiles (P50, P95, P99)
- Error rates by endpoint
- Request volume
- Database connection pool usage
- Memory and CPU usage

### Health Check Monitoring
Set up monitoring that calls `/health` and `/ready` endpoints regularly to ensure service availability.
