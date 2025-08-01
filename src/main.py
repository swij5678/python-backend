"""
Python Service - A sample FastAPI microservice.

This module provides the main entry point for the Python Service,
demonstrating modern Python development practices with FastAPI.
"""

import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models
class ItemCreate(BaseModel):
    """Model for creating a new item."""
    name: str
    description: Optional[str] = None

class ItemResponse(BaseModel):
    """Model for item response."""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    timestamp: datetime
    version: str
    uptime: Optional[int] = None

# Create FastAPI app
app = FastAPI(
    title="Python Service",
    description="A sample Python microservice with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory storage for demo purposes
items_db: Dict[int, Dict[str, Any]] = {}
next_id = 1
start_time = datetime.utcnow()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the service.
    """
    uptime_seconds = int((datetime.utcnow() - start_time).total_seconds())
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime=uptime_seconds
    )

@app.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns whether the service is ready to accept requests.
    """
    return {
        "status": "ready",
        "checks": {
            "database": "ok",  # In a real app, check actual database connection
            "external_api": "ok"
        }
    }

@app.get("/api/v1/items", response_model=List[ItemResponse])
async def get_items(limit: int = 100, offset: int = 0, search: Optional[str] = None):
    """
    Get all items with optional pagination and search.
    
    Args:
        limit: Maximum number of items to return
        offset: Number of items to skip
        search: Search term to filter items
    
    Returns:
        List of items matching the criteria
    """
    logger.info(f"Getting items with limit={limit}, offset={offset}, search={search}")
    
    items = list(items_db.values())
    
    # Apply search filter if provided
    if search:
        items = [
            item for item in items 
            if search.lower() in item["name"].lower() or 
               (item["description"] and search.lower() in item["description"].lower())
        ]
    
    # Apply pagination
    paginated_items = items[offset:offset + limit]
    
    return paginated_items

@app.get("/api/v1/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """
    Get a specific item by ID.
    
    Args:
        item_id: The ID of the item to retrieve
    
    Returns:
        The requested item
    
    Raises:
        HTTPException: If item is not found
    """
    logger.info(f"Getting item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    
    return items_db[item_id]

@app.post("/api/v1/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """
    Create a new item.
    
    Args:
        item: The item data to create
    
    Returns:
        The created item with assigned ID and timestamps
    """
    global next_id
    
    logger.info(f"Creating new item: {item.name}")
    
    now = datetime.utcnow()
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "created_at": now,
        "updated_at": now
    }
    
    items_db[next_id] = new_item
    next_id += 1
    
    logger.info(f"Created item with ID: {new_item['id']}")
    return new_item

@app.put("/api/v1/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate):
    """
    Update an existing item.
    
    Args:
        item_id: The ID of the item to update
        item: The updated item data
    
    Returns:
        The updated item
    
    Raises:
        HTTPException: If item is not found
    """
    logger.info(f"Updating item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found for update: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update the item
    existing_item = items_db[item_id]
    existing_item.update({
        "name": item.name,
        "description": item.description,
        "updated_at": datetime.utcnow()
    })
    
    logger.info(f"Updated item with ID: {item_id}")
    return existing_item

@app.delete("/api/v1/items/{item_id}")
async def delete_item(item_id: int):
    """
    Delete an item by ID.
    
    Args:
        item_id: The ID of the item to delete
    
    Returns:
        Success message
    
    Raises:
        HTTPException: If item is not found
    """
    logger.info(f"Deleting item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found for deletion: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_db[item_id]
    logger.info(f"Deleted item with ID: {item_id}")
    
    return {"message": "Item deleted successfully"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An internal server error occurred"
        }
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting Python Service on port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )
