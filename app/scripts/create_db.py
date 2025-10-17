"""
Database initialization script.
Run this to create all tables in the database.

Usage:
    python -m app.scripts.create_db
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# IMPORTANT: Load .env BEFORE importing app modules
from dotenv import load_dotenv
load_dotenv()

# Now import app modules (db.py will find DATABASE_URL)
from app.db import create_tables, drop_tables, engine
from sqlalchemy import text


def init_db():
    """Initialize the database with all tables"""
    print("🚀 Initializing FitForge database...")
    
    # Test connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL: {version}")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)
    
    # Create tables
    try:
        create_tables()
        print("✅ Database initialization complete!")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        sys.exit(1)


def reset_db():
    """Drop and recreate all tables (DESTRUCTIVE!)"""
    response = input("⚠️  This will DELETE all data. Are you sure? (yes/no): ")
    if response.lower() == "yes":
        print("🗑️  Dropping all tables...")
        drop_tables()
        print("🚀 Recreating all tables...")
        create_tables()
        print("✅ Database reset complete!")
    else:
        print("❌ Operation cancelled.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables (DESTRUCTIVE!)"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        reset_db()
    else:
        init_db()