# Development Guide

This guide covers the development workflow, coding standards, and best practices for the Python Service.

## Development Workflow

### Git Workflow

We follow the [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) branching model:

1. **main**: Production-ready code
2. **develop**: Integration branch for features
3. **feature/***: New features
4. **hotfix/***: Critical fixes for production
5. **release/***: Release preparation

### Branch Naming Convention

- `feature/description-of-feature`
- `bugfix/description-of-bug`
- `hotfix/description-of-hotfix`
- `release/version-number`

### Commit Messages

Follow [Conventional Commits](https://conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
```
feat: add user authentication endpoint
fix(api): handle null values in item description
docs: update API documentation
test: add integration tests for items API
```

## Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

- **Line Length**: 88 characters (Black formatter default)
- **Imports**: Use absolute imports, group them properly
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Required for all public functions

### Code Formatting

We use these tools for consistent code formatting:

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Remove unused imports
autoflake --remove-all-unused-imports --recursive src tests
```

### Linting

```bash
# Check code style
flake8 src tests

# Type checking
mypy src

# Security linting
bandit -r src
```

## Project Structure

```
python-service/
├── src/                    # Source code
│   ├── api/               # API routes and handlers
│   ├── core/              # Core application logic
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── main.py           # Application entry point
├── tests/                 # Test files
│   ├── conftest.py       # Pytest configuration
│   ├── test_api.py       # API tests
│   └── test_services.py  # Service tests
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore patterns
├── .pre-commit-config.yaml # Pre-commit hooks
├── pyproject.toml       # Project configuration
└── README.md            # Project overview
```

## Testing

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database interactions
- **End-to-End Tests**: Test complete user workflows

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests matching a pattern
pytest -k "test_create"

# Run tests with verbose output
pytest -v
```

### Test Configuration

`conftest.py` contains shared fixtures:

```python
@pytest.fixture
def client():
    """Test client for API tests."""
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)

@pytest.fixture
def sample_item():
    """Sample item for testing."""
    return {
        "name": "Test Item",
        "description": "A test item"
    }
```

### Writing Tests

Example test structure:

```python
def test_create_item(client, sample_item):
    """Test creating a new item."""
    # Arrange
    # (sample_item fixture provides test data)
    
    # Act
    response = client.post("/api/v1/items", json=sample_item)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert "id" in data
```

## Database Management

### Migrations

We use Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Database Models

Use SQLAlchemy ORM models:

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Environment Configuration

### Environment Variables

Use environment variables for configuration:

```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Development Environment

Create a `.env` file:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./app.db
```

## Logging

### Configuration

```python
import logging
from src.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Usage

```python
logger.info("Processing request for item %s", item_id)
logger.warning("Item not found: %s", item_id)
logger.error("Database connection failed", exc_info=True)
```

## Performance Optimization

### Database Optimization

- Use database indexes for frequently queried columns
- Implement connection pooling
- Use async database operations where possible

### API Optimization

- Implement response caching
- Use pagination for large datasets
- Add request/response compression

### Monitoring

- Add metrics collection with Prometheus
- Implement distributed tracing
- Set up health checks

## Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

Install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

## Debugging

### Local Debugging

Use VS Code debugging configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "src/main.py",
      "console": "integratedTerminal",
      "env": {
        "DEBUG": "true"
      }
    }
  ]
}
```

### Docker Debugging

Enable debugging in Docker:

```dockerfile
# Add to Dockerfile for development
RUN pip install debugpy
EXPOSE 5678
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client src/main.py
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/project/src"
```

**Database Connection Issues**
```bash
# Check database status
python -c "from src.database import engine; print(engine.execute('SELECT 1').scalar())"
```

**Dependency Conflicts**
```bash
# Check for conflicts
pip check

# Update all packages
pip-upgrade-requirements requirements.txt
```

### Debug Commands

```bash
# Check API health
curl http://localhost:8000/health

# View logs
tail -f logs/app.log

# Check database tables
sqlite3 app.db ".tables"

# Monitor resource usage
htop
```

## Documentation

### Code Documentation

Use Google-style docstrings:

```python
def create_item(item_data: dict) -> Item:
    """Create a new item.

    Args:
        item_data: Dictionary containing item information.

    Returns:
        Created item instance.

    Raises:
        ValidationError: If item data is invalid.
    """
```

### API Documentation

Update OpenAPI schemas in your FastAPI endpoints:

```python
@app.post("/api/v1/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item.
    
    Creates a new item with the provided information.
    """
```

## Deployment

See the [Deployment Guide](deployment.md) for detailed deployment instructions.

## Contributing

See the [Contributing Guide](contributing.md) for information on how to contribute to this project.
