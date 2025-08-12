# API Changelog

All notable changes to the Python Service API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Authentication and authorization endpoints
- Bulk operations for items
- Item categories and tags
- Advanced filtering and sorting options
- Rate limiting headers
- API versioning in headers

## [1.0.0] - 2025-08-11

### Added
- Initial API release
- Health check endpoint (`/health`)
- Readiness check endpoint (`/ready`)
- Items CRUD API at `/api/v1/items`
  - `GET /api/v1/items` - List items with pagination and search
  - `POST /api/v1/items` - Create new item
  - `GET /api/v1/items/{id}` - Get item by ID
  - `PUT /api/v1/items/{id}` - Update item
  - `DELETE /api/v1/items/{id}` - Delete item
- OpenAPI 3.0 specification
- Postman collection for testing
- Comprehensive error handling
- Request/response validation
- Automatic API documentation generation

### Endpoints Details

#### Health Endpoints
- **GET /health**
  - Returns service health status, version, and uptime
  - Response: `HealthResponse` schema
  - Status codes: 200

- **GET /ready**
  - Returns service readiness with dependency checks
  - Response: Object with status and checks
  - Status codes: 200

#### Items API (v1)
- **GET /api/v1/items**
  - Query parameters: `limit` (1-1000, default 100), `offset` (default 0), `search` (optional)
  - Response: Array of `ItemResponse` objects
  - Status codes: 200, 400

- **POST /api/v1/items**
  - Request body: `ItemCreate` schema
  - Response: `ItemResponse` schema
  - Status codes: 201, 400, 422

- **GET /api/v1/items/{item_id}**
  - Path parameter: `item_id` (integer)
  - Response: `ItemResponse` schema
  - Status codes: 200, 404

- **PUT /api/v1/items/{item_id}**
  - Path parameter: `item_id` (integer)
  - Request body: `ItemCreate` schema
  - Response: `ItemResponse` schema
  - Status codes: 200, 400, 404, 422

- **DELETE /api/v1/items/{item_id}**
  - Path parameter: `item_id` (integer)
  - Response: Success message object
  - Status codes: 200, 404

### Data Models

#### ItemCreate
```json
{
  "name": "string (required, 1-255 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

#### ItemResponse
```json
{
  "id": "integer",
  "name": "string",
  "description": "string | null",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

#### HealthResponse
```json
{
  "status": "healthy | unhealthy | degraded",
  "timestamp": "ISO 8601 datetime",
  "version": "semver string",
  "uptime": "integer (seconds) | null"
}
```

### Error Handling
- Consistent error response format
- Proper HTTP status codes
- Detailed validation error messages
- Global exception handling

### Features
- **Pagination**: Items endpoint supports limit/offset pagination
- **Search**: Full-text search across item name and description
- **Validation**: Request validation using Pydantic models
- **Logging**: Comprehensive logging for all operations
- **Documentation**: Auto-generated Swagger UI and ReDoc
- **Health Checks**: Kubernetes-ready health and readiness probes

### Technical Details
- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **Documentation**: OpenAPI 3.0
- **Response Format**: JSON only
- **Datetime Format**: ISO 8601 UTC
- **Character Encoding**: UTF-8

## Version Compatibility

### Breaking Changes Policy
- Major version increments (X.0.0) may include breaking changes
- Minor version increments (0.X.0) are backward compatible with new features
- Patch version increments (0.0.X) are backward compatible bug fixes

### Deprecation Policy
- Features will be marked as deprecated for at least one minor version before removal
- Deprecated features will include alternative recommendations
- Deprecation warnings will be included in API responses when applicable

## Migration Guide

### Future Migrations
This section will be populated as new versions are released with specific migration instructions.

## Support

### API Versions
- **Current**: v1.0.0
- **Supported**: v1.x.x
- **End of Life**: None yet

### Contact
- **Team**: Platform Team
- **Email**: platform@yourorg.com
- **Documentation**: Available at `/docs` and `/redoc` endpoints
