# Contributing to Python Service

Thank you for your interest in contributing to the Python Service! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.9 or higher
- Git
- A GitHub account
- Docker (optional, for testing deployments)

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/python-service.git
   cd python-service
   ```

3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-org/python-service.git
   ```

4. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

6. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

7. **Run tests** to verify setup:
   ```bash
   pytest
   ```

## Development Process

### Workflow Overview

1. **Find or create an issue** to work on
2. **Create a feature branch** from `develop`
3. **Make your changes** with tests
4. **Ensure all tests pass** and code is properly formatted
5. **Submit a pull request** for review
6. **Address feedback** and iterate

### Branch Naming

Use descriptive branch names that include the issue number:

- `feature/123-add-user-authentication`
- `bugfix/456-fix-null-pointer-error`
- `docs/789-update-api-documentation`
- `refactor/101-improve-error-handling`

### Commit Guidelines

Follow [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**
```
feat(api): add user authentication endpoint

Add JWT-based authentication with login/logout endpoints.
Includes middleware for protecting routes and user session management.

Closes #123

fix(database): handle connection timeout gracefully

Previously, database connection timeouts would crash the application.
Now they are caught and handled with appropriate error responses.

Fixes #456

docs: update API documentation for new endpoints

Add documentation for authentication endpoints and update
existing endpoint descriptions with new parameters.
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

#### Code Formatting
- **Line Length**: 88 characters (Black formatter default)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use double quotes for strings
- **Trailing Commas**: Use them in multi-line structures

#### Imports
```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
import fastapi
import sqlalchemy
from pydantic import BaseModel

# Local application imports
from src.core.config import settings
from src.models.user import User
```

#### Type Hints
Type hints are required for all public functions:

```python
from typing import List, Optional, Dict, Any

def get_user_by_id(user_id: int) -> Optional[User]:
    """Get a user by their ID."""
    pass

def create_users(users: List[Dict[str, Any]]) -> List[User]:
    """Create multiple users from a list of user data."""
    pass
```

#### Docstrings
Use Google-style docstrings:

```python
def calculate_total_price(items: List[Item], tax_rate: float = 0.08) -> float:
    """Calculate the total price including tax.

    Args:
        items: List of items to calculate total for.
        tax_rate: Tax rate to apply (default: 0.08 for 8%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If tax_rate is negative.
        
    Example:
        >>> items = [Item(price=10.0), Item(price=20.0)]
        >>> calculate_total_price(items, 0.1)
        33.0
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

### Code Quality Tools

Run these tools before submitting:

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Check style
flake8 src tests

# Type checking
mypy src

# Security check
bandit -r src
```

## Testing Guidelines

### Test Structure

Tests should be organized to mirror the source code structure:

```
tests/
├── conftest.py           # Shared fixtures
├── test_api/
│   ├── test_health.py    # Health endpoint tests
│   ├── test_items.py     # Items API tests
│   └── test_auth.py      # Authentication tests
├── test_services/
│   ├── test_item_service.py
│   └── test_user_service.py
└── test_utils/
    └── test_validators.py
```

### Test Types

#### Unit Tests
Test individual functions and classes in isolation:

```python
import pytest
from src.services.item_service import ItemService
from src.models.item import Item

def test_create_item():
    """Test creating a new item."""
    service = ItemService()
    item_data = {"name": "Test Item", "description": "A test item"}
    
    result = service.create_item(item_data)
    
    assert isinstance(result, Item)
    assert result.name == "Test Item"
    assert result.id is not None
```

#### Integration Tests
Test API endpoints and database interactions:

```python
def test_create_item_endpoint(client, sample_item):
    """Test the create item API endpoint."""
    response = client.post("/api/v1/items", json=sample_item)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert "id" in data
    assert "created_at" in data
```

#### Test Fixtures
Use pytest fixtures for common test data:

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    """Test client for API tests."""
    return TestClient(app)

@pytest.fixture
def sample_item():
    """Sample item data for testing."""
    return {
        "name": "Test Item",
        "description": "A test item for testing purposes"
    }

@pytest.fixture
def authenticated_user(client):
    """Create and return an authenticated user."""
    user_data = {"username": "testuser", "password": "testpass"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### Test Coverage

Maintain high test coverage:

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Coverage should be at least 80%
pytest --cov=src --cov-fail-under=80
```

### Test Naming

Use descriptive test names that explain what is being tested:

```python
def test_create_item_with_valid_data_returns_created_item():
    """Test that creating an item with valid data returns the created item."""
    pass

def test_create_item_with_missing_name_raises_validation_error():
    """Test that creating an item without a name raises ValidationError."""
    pass

def test_get_item_by_id_with_nonexistent_id_returns_404():
    """Test that getting a non-existent item returns 404."""
    pass
```

## Documentation

### Code Documentation

- Write clear docstrings for all public functions and classes
- Include examples in docstrings when helpful
- Document complex algorithms and business logic
- Keep comments up-to-date with code changes

### API Documentation

- Update OpenAPI schemas when adding/modifying endpoints
- Include request/response examples
- Document error responses
- Add descriptions for all parameters

### User Documentation

When making changes that affect users:

- Update relevant documentation in `docs/`
- Add examples and use cases
- Update the changelog
- Consider adding screenshots for UI changes

## Pull Request Process

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Run all checks**:
   ```bash
   # Run tests
   pytest

   # Check code quality
   black --check src tests
   isort --check-only src tests
   flake8 src tests
   mypy src
   ```

3. **Update documentation** if needed

### Pull Request Template

Use this template for your pull request description:

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Code is well-commented
- [ ] Documentation updated
- [ ] No new warnings introduced

## Related Issues
Closes #issue_number

## Screenshots (if applicable)
Add screenshots here if the change affects the UI.
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Testing** in staging environment (if applicable)
4. **Approval** from project maintainers
5. **Merge** by maintainers

### Addressing Feedback

When reviewers request changes:

1. Make the requested changes
2. Add commits to your branch (don't force-push)
3. Respond to review comments
4. Request another review when ready

## Issue Reporting

### Bug Reports

When reporting bugs, include:

**Environment Information:**
- Python version
- Operating system
- Dependency versions
- Configuration details

**Bug Description:**
- What you expected to happen
- What actually happened
- Steps to reproduce
- Error messages and stack traces

**Example Bug Report:**
```markdown
**Environment:**
- Python 3.9.7
- Ubuntu 20.04
- FastAPI 0.68.0

**Description:**
When creating an item with a very long description (>1000 characters), 
the API returns a 500 error instead of a validation error.

**Expected Behavior:**
Should return a 422 validation error with details about the field length limit.

**Actual Behavior:**
Returns a 500 internal server error.

**Steps to Reproduce:**
1. Send POST request to `/api/v1/items`
2. Include description field with 1001 characters
3. Observe the 500 error response

**Error Message:**
```
Internal Server Error: field 'description' exceeds maximum length
```
```

### Feature Requests

When requesting features, include:

- **Problem description**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you consider?
- **Use cases**: When would this be used?

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Slack/Discord**: Real-time chat with the community
- **Email**: security@yourorg.com for security issues

### Getting Help

If you need help:

1. Check the [documentation](index.md)
2. Search existing [issues](https://github.com/your-org/python-service/issues)
3. Ask in [discussions](https://github.com/your-org/python-service/discussions)
4. Join the community chat

### Recognition

Contributors are recognized in:

- The project README
- Release notes
- The contributors page
- Social media shout-outs

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (typically MIT or Apache 2.0).

---

Thank you for contributing to the Python Service! Your efforts help make this project better for everyone. 🎉
