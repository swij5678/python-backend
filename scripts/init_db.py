#!/usr/bin/env python3
"""
Database initialization script.

This script initializes the database for the Python Service.
In this simple version, it just creates an empty SQLite database file.
"""

import os
import sqlite3
from pathlib import Path


def init_database():
    """Initialize the database."""
    # Create the database file if it doesn't exist
    db_path = Path("app.db")
    
    if db_path.exists():
        print(f"Database {db_path} already exists.")
        return
    
    # Create the database file
    conn = sqlite3.connect(str(db_path))
    
    # Create items table (example)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create an index on name for faster searches
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_name ON items(name)")
    
    conn.commit()
    conn.close()
    
    print(f"Database {db_path} initialized successfully.")


if __name__ == "__main__":
    init_database()
