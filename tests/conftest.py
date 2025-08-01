"""
Test configuration and shared fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_item():
    """Sample item data for testing."""
    return {
        "name": "Test Item",
        "description": "A test item for testing purposes"
    }


@pytest.fixture
def sample_items():
    """Multiple sample items for testing."""
    return [
        {"name": "Item 1", "description": "First test item"},
        {"name": "Item 2", "description": "Second test item"},
        {"name": "Item 3", "description": "Third test item"},
    ]


@pytest.fixture(autouse=True)
def reset_items_db():
    """Reset the items database before each test."""
    from src.main import items_db, next_id
    items_db.clear()
    # Reset the next_id counter
    import src.main
    src.main.next_id = 1
