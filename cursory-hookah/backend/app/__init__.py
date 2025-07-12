from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hookah_gear.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Import and register blueprints
    from app.routes.gear import gear_bp
    from app.routes.user import user_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.scraper import scraper_bp
    
    app.register_blueprint(gear_bp, url_prefix='/api/gear')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    app.register_blueprint(scraper_bp, url_prefix='/api/scraper')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize sample data if database is empty
        from app.models.gear import Gear
        if Gear.query.count() == 0:
            from app.services.sample_data import initialize_sample_data
            initialize_sample_data()
    
    return app 