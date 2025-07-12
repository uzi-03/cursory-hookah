#!/usr/bin/env python3
"""
Reset database and reload sample data with new image URLs
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.gear import Gear

def reset_database():
    """Reset the database and reload sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("🗑️  Dropped all database tables")
        
        # Create all tables
        db.create_all()
        print("✅ Created new database tables")
        
        # Import and run sample data initialization
        from app.services.sample_data import initialize_sample_data
        initialize_sample_data()
        
        # Verify the data was loaded
        gear_count = Gear.query.count()
        print(f"✅ Loaded {gear_count} gear items with new image URLs")
        
        # Show some sample items
        sample_items = Gear.query.limit(3).all()
        print("\n📸 Sample items with new images:")
        for item in sample_items:
            print(f"  - {item.name}: {item.image_url}")

if __name__ == "__main__":
    print("🔄 Resetting database and reloading sample data...")
    reset_database()
    print("\n🎉 Database reset complete! New images should now load properly.") 