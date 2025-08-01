# Getting Started

This guide will help you set up the Python Service development environment and run the service locally.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher**: [Download Python](https://python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker** (optional): [Download Docker](https://docker.com/get-started)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/python-service.git
cd python-service
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Application settings
DEBUG=true
LOG_LEVEL=INFO

# Database settings
DATABASE_URL=sqlite:///./app.db

# API settings
API_VERSION=v1
API_PREFIX=/api/v1
```

### 5. Initialize the Database

```bash
# Run database migrations
python scripts/init_db.py
```

## Running the Service

### Development Mode

```bash
# Start the development server
python src/main.py
```

The service will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Using Docker

```bash
# Build the Docker image
docker build -t python-service .

# Run the container
docker run -p 8000:8000 python-service
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d
```

## Verification

### Health Check

Verify the service is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-31T10:00:00Z",
  "version": "1.0.0"
}
```

### API Test

Test the items endpoint:

```bash
# Get all items
curl http://localhost:8000/api/v1/items

# Create a new item
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item"}'
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_api.py
```

## Development Tools

### Code Formatting

```bash
# Format code with black
black src tests

# Sort imports
isort src tests
```

### Linting

```bash
# Run flake8 linting
flake8 src tests

# Run mypy type checking
mypy src
```

## Next Steps

Now that you have the service running:

1. Explore the [API Reference](api-reference.md)
2. Read the [Development Guide](development.md)
3. Check out the [Deployment Instructions](deployment.md)

## Troubleshooting

### Common Issues

**Import Errors**
- Ensure your virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Database Connection Errors**
- Check your DATABASE_URL in the `.env` file
- Ensure the database is running (if using PostgreSQL/MySQL)

**Port Already in Use**
- Change the port in the configuration or stop the conflicting service
- Use `netstat -tulpn | grep 8000` to find what's using port 8000

### Getting Help

If you encounter issues:

1. Check the logs: `tail -f logs/app.log`
2. Review the [troubleshooting section](development.md#troubleshooting)
3. Open an issue on GitHub
