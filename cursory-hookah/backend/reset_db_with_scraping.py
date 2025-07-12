#!/usr/bin/env python3
"""
Reset database and add source_website field for real scraping
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app import create_app, db
from app.models.gear import Gear
from app.models.user import User, UserGear
from app.services.sample_data import initialize_sample_data

def reset_database():
    """Reset the database and reload sample data"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()
        
        print("🏗️  Creating new tables...")
        db.create_all()
        
        print("📝 Adding sample data...")
        initialize_sample_data()
        
        # Create a sample user
        user = User(username='demo_user', email='demo@example.com')
        db.session.add(user)
        
        try:
            db.session.commit()
            print(f"✅ Database reset complete!")
            print(f"📊 Added sample products")
            print(f"👤 Added 1 demo user")
            
            # Verify the data
            total_gear = Gear.query.count()
            total_users = User.query.count()
            print(f"📈 Database now contains:")
            print(f"   - {total_gear} gear items")
            print(f"   - {total_users} users")
            
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Starting database reset...")
    success = reset_database()
    
    if success:
        print("\n🎉 Database reset successful!")
        print("💡 You can now run the scraper to add real products from hookah websites.")
        print("   python run.py")
    else:
        print("\n❌ Database reset failed!")
        sys.exit(1) 