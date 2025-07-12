from flask import Blueprint, jsonify, request
from app.services.scraper import HookahScraper
from app import db

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/trigger', methods=['POST'])
def trigger_scraping():
    """Trigger product scraping from configured websites"""
    try:
        data = request.get_json() or {}
        website = data.get('website', 'demo')  # Default to demo scraping
        
        scraper = HookahScraper()
        
        if website == 'demo':
            # Run demo scraping with sample data
            results = scraper.scrape_demo()
        else:
            # Run actual scraping (implemented later)
            results = scraper.scrape_website(website)
        
        return jsonify({
            'success': True,
            'message': f'Scraping completed for {website}',
            'data': {
                'products_found': len(results),
                'website': website
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scraper_bp.route('/status', methods=['GET'])
def get_scraping_status():
    """Get current scraping status and statistics"""
    try:
        from app.models.gear import Gear
        
        # Get basic statistics
        total_products = Gear.query.count()
        categories = db.session.query(Gear.category).distinct().all()
        brands = db.session.query(Gear.brand).distinct().all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_products': total_products,
                'categories': len(categories),
                'brands': len(brands),
                'last_updated': '2024-01-01'  # TODO: Add actual tracking
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 