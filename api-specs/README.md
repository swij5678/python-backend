# API Specifications

This folder contains the API specification documents for the Python Service.

## Files

### `openapi.yaml`
Complete OpenAPI 3.0 specification for all endpoints, including:
- Health and readiness checks
- Full CRUD operations for items
- Request/response schemas
- Error handling documentation

### `schemas.yaml`
Separated schema definitions for better maintainability and reusability across different API versions.

### `postman-collection.json`
Postman collection with example requests for all endpoints, useful for testing and development.

### `api-changelog.md`
Documentation of API changes across different versions.

## Usage

### Viewing the API Documentation
1. **Swagger UI**: Available at `http://localhost:8000/docs` when running the service
2. **ReDoc**: Available at `http://localhost:8000/redoc` when running the service
3. **Static Documentation**: Use tools like [Swagger Editor](https://editor.swagger.io/) to view the OpenAPI spec

### Generating Client Code
You can use the OpenAPI specification to generate client libraries in various languages:

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python client
openapi-generator-cli generate -i api-specs/openapi.yaml -g python -o clients/python

# Generate JavaScript client
openapi-generator-cli generate -i api-specs/openapi.yaml -g javascript -o clients/javascript

# Generate TypeScript client
openapi-generator-cli generate -i api-specs/openapi.yaml -g typescript-fetch -o clients/typescript
```

### Validation
Validate the OpenAPI specification:

```bash
# Using swagger-codegen
swagger-codegen validate -i api-specs/openapi.yaml

# Using openapi-generator
openapi-generator-cli validate -i api-specs/openapi.yaml
```

## API Overview

### Base URL
- **Local Development**: `http://localhost:8000`
- **Production**: `https://api.example.com`

### Authentication
Currently, the API does not require authentication. For production use, consider implementing:
- JWT tokens
- API keys
- OAuth 2.0

### Endpoints Summary

#### Health Endpoints
- `GET /health` - Service health check
- `GET /ready` - Service readiness check

#### Items API (v1)
- `GET /api/v1/items` - List items with pagination and search
- `POST /api/v1/items` - Create new item
- `GET /api/v1/items/{id}` - Get item by ID
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Response Formats
All responses are in JSON format. Error responses follow a consistent structure:

```json
{
  "error": "error_code",
  "message": "Human readable error message",
  "detail": "Additional error details"
}
```

### Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Version History
- **v1.0.0** - Initial API version with basic CRUD operations for items

## Contributing
When updating the API:
1. Update the OpenAPI specification
2. Update the changelog
3. Increment the version number
4. Test all endpoints
5. Update client libraries if needed
