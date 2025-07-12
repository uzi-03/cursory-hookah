from flask import Blueprint, jsonify, request
from app.services.scraper import HookahScraper
from app.services.real_scrapers import RealHookahScraper
from app import db

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/trigger', methods=['POST'])
def trigger_scraping():
    """Trigger product scraping from configured websites"""
    try:
        data = request.get_json() or {}
        website = data.get('website', 'demo')  # Default to demo scraping
        category = data.get('category')
        max_pages = data.get('max_pages', 2)
        
        if website == 'demo':
            scraper = HookahScraper()
            results = scraper.scrape_demo()
            products_found = len(results.get('products', []))
        else:
            real_scraper = RealHookahScraper()
            
            if website == 'all':
                # Scrape all websites
                products = real_scraper.scrape_all_websites(
                    categories=[category] if category else None,
                    max_pages=max_pages
                )
            else:
                # Scrape specific website
                products = real_scraper.scrape_website(
                    website, 
                    category=category, 
                    max_pages=max_pages
                )
            
            # Save products to database
            results = real_scraper.save_products_to_db(products)
            products_found = results.get('added', 0) + results.get('updated', 0)
        
        return jsonify({
            'success': True,
            'message': f'Scraping completed for {website}',
            'data': {
                'products_found': products_found,
                'website': website,
                'category': category,
                'details': results
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
        websites = db.session.query(Gear.source_website).distinct().all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_products': total_products,
                'categories': len(categories),
                'brands': len(brands),
                'websites': len(websites),
                'last_updated': '2024-01-01'  # TODO: Add actual tracking
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scraper_bp.route('/websites', methods=['GET'])
def get_available_websites():
    """Get list of available websites for scraping"""
    try:
        websites = [
            {
                'name': 'southsmoke',
                'display_name': 'SouthSmoke.com',
                'url': 'https://www.southsmoke.com',
                'categories': ['hookah', 'bowl', 'hose', 'hmd']
            },
            {
                'name': '5starhookah',
                'display_name': '5StarHookah.com',
                'url': 'https://5starhookah.com',
                'categories': ['hookah', 'bowl', 'hose', 'hmd', 'tobacco', 'coal', 'accessory']
            },
            {
                'name': 'sobehookah',
                'display_name': 'SobeHookah.com',
                'url': 'https://www.sobehookah.com',
                'categories': ['hookah', 'bowl', 'hose', 'hmd']
            }
        ]
        
        return jsonify({
            'success': True,
            'data': websites
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 