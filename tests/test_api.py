"""
Tests for the main API endpoints.
"""

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data


def test_readiness_endpoint(client):
    """Test the readiness check endpoint."""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "checks" in data
    assert data["checks"]["database"] == "ok"


def test_get_items_empty(client):
    """Test getting items when database is empty."""
    response = client.get("/api/v1/items")
    
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_create_item(client, sample_item):
    """Test creating a new item."""
    response = client.post("/api/v1/items", json=sample_item)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert data["description"] == sample_item["description"]
    assert data["id"] == 1
    assert "created_at" in data
    assert "updated_at" in data


def test_create_item_without_description(client):
    """Test creating an item without description."""
    item_data = {"name": "Test Item"}
    response = client.post("/api/v1/items", json=item_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] is None


def test_get_item_by_id(client, sample_item):
    """Test getting a specific item by ID."""
    # First create an item
    create_response = client.post("/api/v1/items", json=sample_item)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Then get it by ID
    response = client.get(f"/api/v1/items/{item_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == sample_item["name"]


def test_get_nonexistent_item(client):
    """Test getting an item that doesn't exist."""
    response = client.get("/api/v1/items/999")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"


def test_update_item(client, sample_item):
    """Test updating an existing item."""
    # First create an item
    create_response = client.post("/api/v1/items", json=sample_item)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Update the item
    updated_data = {
        "name": "Updated Item",
        "description": "Updated description"
    }
    response = client.put(f"/api/v1/items/{item_id}", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "Updated description"
    assert data["id"] == item_id


def test_update_nonexistent_item(client):
    """Test updating an item that doesn't exist."""
    update_data = {"name": "Updated Item"}
    response = client.put("/api/v1/items/999", json=update_data)
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"


def test_delete_item(client, sample_item):
    """Test deleting an item."""
    # First create an item
    create_response = client.post("/api/v1/items", json=sample_item)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/items/{item_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item deleted successfully"
    
    # Verify item is deleted
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_item(client):
    """Test deleting an item that doesn't exist."""
    response = client.delete("/api/v1/items/999")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"


def test_get_items_with_pagination(client, sample_items):
    """Test getting items with pagination."""
    # Create multiple items
    for item in sample_items:
        client.post("/api/v1/items", json=item)
    
    # Test pagination
    response = client.get("/api/v1/items?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Test second page
    response = client.get("/api/v1/items?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_search_items(client, sample_items):
    """Test searching items by name or description."""
    # Create multiple items
    for item in sample_items:
        client.post("/api/v1/items", json=item)
    
    # Search by name
    response = client.get("/api/v1/items?search=Item 1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Item 1"
    
    # Search by description
    response = client.get("/api/v1/items?search=First")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "First" in data[0]["description"]
